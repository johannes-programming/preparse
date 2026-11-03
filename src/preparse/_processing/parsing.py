__all__: list[str] = ["parse"]

from collections.abc import Iterable
from types import FunctionType
from typing import Any, Generator

from preparse._items.Bundle import Bundle
from preparse._items.Item import Item
from preparse._items.Long import Long
from preparse._items.Option import Option
from preparse._items.Special import Special
from preparse.abc.Message import Message
from preparse._option_spec import (
    NO_ARGUMENT, OPTIONAL_ARGUMENT, REQUIRED_ARGUMENT
)
from preparse.messaging.AmbiguousOptionMessage import (
    AmbiguousOptionMessage as PAOW,
)
from preparse.messaging.InvalidOptionMessage import (
    InvalidOptionMessage as PIOW,
)
from preparse.messaging.RequiredArgumentMessage import (
    RequiredArgumentMessage as PRAW,
)
from preparse.messaging.UnallowedArgumentMessage import (
    UnallowedArgumentMessage as PUAW,
)


def parse(args: list[Item], **kwargs: Any) -> tuple[list[Item], list[Message]]:
    messages: list[Message]
    messages = list()

    def warn(message: Message, /) -> None:
        messages.append(message)

    preparsed = list(parse_generator(args, warn=warn, **kwargs))
    return preparsed, messages


def parse_bundling(
    arg: str,
    *,
    cause: FunctionType,
    modes: dict[Any, Any],
) -> Bundle:
    ans: Bundle
    x: int
    y: str
    ans = Bundle(chars="", nargs=NO_ARGUMENT)
    for x, y in enumerate(arg):
        if x == 0:
            continue
        ans.chars += y
        ans.nargs = modes.get("-" + y, NO_ARGUMENT)
        if "-" + y not in modes:
            cause(PIOW, option=y, islong=False)
        if ans.nargs == NO_ARGUMENT:
            continue
        if ans.nargs == OPTIONAL_ARGUMENT or x < len(arg) - 1:
            ans.joined = True
            ans.right = arg[x + 1 :]
        return ans
    return ans


def parse_cause(
    *,
    prog: str,
    warn: FunctionType,
) -> Any:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_generator(
    items: list[Any],
    *,
    has_longopts: bool,
    has_shortopts: bool,
    expectsabbr: bool,
    expectsposix: bool,
    modes: dict[Any, Any],
    prog: str,
    warn: FunctionType,
) -> Generator[Any, Any, Any]:
    broken: bool
    cause: FunctionType
    item: Any
    last: Any
    broken = not (has_longopts or has_shortopts)
    cause = parse_cause(prog=prog, warn=warn)
    last = None
    for item in items:
        if broken:
            # if we are in the positional-only part
            yield item
            continue
        if last is not None:
            # if the last item hungers for a value
            last.right = item.value
            last.joined = False
            yield last
            last = None
            continue
        if item.value == "--":
            yield Special()
            broken = True
            continue
        if item.isobvious():
            # if the item is positional
            yield item
            broken = expectsposix
            continue
        last = parse_option(
            item.value,
            has_longopts=has_longopts,
            has_shortopts=has_shortopts,
            cause=cause,
            expectsabbr=expectsabbr,
            modes=modes,
        )
        if not last.ishungry():
            yield last
            last = None
    if last is None:
        # if the last item is not starved
        return
    if isinstance(last, Long):
        cause(PRAW, option=last.fullkey, islong=True)
    else:
        cause(PRAW, option=last.chars[-1], islong=False)
    yield last


def parse_islong(
    arg: str,
    *,
    has_longopts: bool,
    has_shortopts: bool,
) -> bool:
    if has_longopts and has_shortopts:
        return arg.startswith("--")
    else:
        return not has_shortopts


def parse_long(
    arg: str,
    *,
    cause: FunctionType,
    expectsabbr: bool,
    modes: dict[Any, Any],
) -> Long:
    ans: Long
    parts: list[str]
    parts = arg.split("=", 1)
    ans = Long(fullkey=parts.pop(0))
    if len(parts):
        ans.joined = True
        ans.right = parts.pop()
    ans.abbrlen = len(ans.fullkey)
    if ans.fullkey in modes.keys():
        parts = [ans.fullkey]
    elif expectsabbr:
        parts = parse_long_startswith(ans.abbr, keys=modes.keys())
    else:
        parts = list()  # can be assumed
    if len(parts) == 0:
        ans.nargs = OPTIONAL_ARGUMENT
        cause(PIOW, option=arg, islong=True)
        return ans
    if len(parts) >= 2:
        ans.nargs = OPTIONAL_ARGUMENT
        cause(PAOW, option=arg, possibilities=parts)
        return ans
    (ans.fullkey,) = parts
    ans.nargs = modes[ans.fullkey]
    if (ans.nargs == NO_ARGUMENT) and (ans.right is not None):
        cause(PUAW, option=ans.fullkey)
    return ans


def parse_long_startswith(
    abbr: str,
    *,
    keys: Iterable[str],
) -> list[str]:
    ans: list[str]
    x: str
    ans = list()
    for x in keys:
        if x.startswith(abbr):
            ans.append(x)
    return ans


def parse_option(
    arg: str,
    *,
    cause: FunctionType,
    expectsabbr: bool,
    modes: dict[Any, Any],
    **kwargs: Any,
) -> Option:
    if parse_islong(arg, **kwargs):
        return parse_long(
            arg,
            cause=cause,
            expectsabbr=expectsabbr,
            modes=modes,
        )
    else:
        return parse_bundling(
            arg,
            cause=cause,
            modes=modes,
        )

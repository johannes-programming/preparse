__all__: list[str] = ["parse"]

from types import FunctionType
from typing import Any, Generator

from preparse._items.Bundle import Bundle
from preparse._items.Item import Item
from preparse._items.Long import Long
from preparse._items.Option import Option
from preparse._items.Special import Special
from preparse.abc.Message import Message
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
    shortopts: str,
) -> Bundle:
    ans: Bundle
    x: int
    y: str
    ans = Bundle(chars="", argmode="")
    for x, y in enumerate(arg):
        if x == 0:
            continue
        ans.chars += y
        mode = short_argmode(y, shortopts)
        if mode is None:
            cause(PIOW, option=y, islong=False)
            continue
        ans.argmode = mode
        if mode == "":
            continue
        if mode == "::" or x < len(arg) - 1:
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
    shortopts: str | None,
    longopts: tuple[str, ...] | None,
    is_posix: bool,
    prog: str,
    warn: FunctionType,
) -> Generator[Any, Any, Any]:
    broken: bool
    cause: FunctionType
    item: Any
    last: Any
    broken = shortopts is None and longopts is None
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
            broken = is_posix
            continue
        last = parse_option(
            item.value,
            shortopts=shortopts,
            longopts=longopts,
            cause=cause,
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
    shortopts: str | None,
    longopts: tuple[str, ...] | None,
) -> bool:
    if longopts is not None and shortopts is not None:
        return arg.startswith("--")
    return shortopts is None


def short_argmode(option: str, shortopts: str) -> str | None:
    """Read a short-option spec: no suffix, :, or :: (optional)."""
    for index, char in enumerate(shortopts):
        if char == option and char != ":":
            if shortopts[index + 1 : index + 3] == "::":
                return "::"
            if shortopts[index + 1 : index + 2] == ":":
                return ":"
            return ""
    return None


def long_argmode(spec: str) -> tuple[str, str]:
    """Read a long-option spec: no suffix, =, or =? (optional)."""
    if spec.endswith("=?"):
        return spec[:-2], "::"
    if spec.endswith("="):
        return spec[:-1], ":"
    return spec, ""


def parse_long(
    arg: str,
    *,
    cause: FunctionType,
    longopts: tuple[str, ...],
) -> Long:
    parts = arg.split("=", 1)
    ans = Long(fullkey=parts.pop(0))
    if parts:
        ans.joined = True
        ans.right = parts.pop()
    ans.abbrlen = len(ans.fullkey)
    # Match using the full spelling, preserving legacy single-dash long
    # names rather than allowing them to match '--' abbreviations.
    options = [
        (key if key.startswith("-") else "--" + key, mode)
        for key, mode in (long_argmode(spec) for spec in longopts)
    ]
    matches = [(key, mode) for key, mode in options if key == ans.fullkey]
    if matches:
        # getopt prefers an exact bare name over its argument variants.
        matches = [
            min(matches, key=lambda match: ("", ":", "::").index(match[1]))
        ]
    else:
        matches = [
            (key, mode) for key, mode in options if key.startswith(ans.fullkey)
        ]
    if not matches:
        ans.argmode = "::"
        cause(PIOW, option=arg, islong=True)
        return ans
    if len(matches) >= 2:
        ans.argmode = "::"
        cause(
            PAOW,
            option=arg,
            possibilities=[key for key, _ in matches],
        )
        return ans
    key, ans.argmode = matches[0]
    ans.fullkey = key
    if ans.argmode == "" and ans.right is not None:
        cause(PUAW, option=ans.fullkey)
    return ans


def parse_option(
    arg: str,
    *,
    cause: FunctionType,
    shortopts: str | None,
    longopts: tuple[str, ...] | None,
) -> Option:
    if parse_islong(arg, shortopts=shortopts, longopts=longopts):
        return parse_long(
            arg,
            cause=cause,
            longopts=longopts if longopts is not None else (),
        )
    return parse_bundling(
        arg,
        cause=cause,
        shortopts=shortopts if shortopts is not None else "",
    )

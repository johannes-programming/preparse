from types import FunctionType
from typing import *

from preparse._items.Bundle import Bundle
from preparse._items.Item import Item
from preparse._items.Long import Long
from preparse._items.Option import Option
from preparse._items.Positional import Positional
from preparse._items.Special import Special
from preparse.core import warnings
from preparse.core.enums import *
from datahold import HoldNaming

__all__ = ["parse"]

PAOW = warnings.PreparseAmbiguousOptionWarning
PIOW = warnings.PreparseInvalidOptionWarning
PUAW = warnings.PreparseUnallowedArgumentWarning
PRAW = warnings.PreparseRequiredArgumentWarning


def parse(
    args: list[str],
    **kwargs: Any,
) -> list[Item]:
    return list(parse_generator(args, **kwargs))


def parse_bundling(
    arg: str,
    *,
    cause: FunctionType,
    optNaming: HoldNaming,
) -> Bundle:
    ans: Bundle
    x: int
    y: str
    ans = Bundle(chars="")
    for x, y in enumerate(arg):
        if x == 0:
            continue
        ans.chars += y
        try:
            ans.nargs = optNaming["-" + y]
        except KeyError:
            cause(PIOW, option=y, islong=False)
            ans.nargs = Nargs.NO_ARGUMENT
        if ans.nargs == Nargs.NO_ARGUMENT:
            continue
        if ans.nargs == Nargs.OPTIONAL_ARGUMENT or x < len(arg) - 1:
            ans.joined = True
            ans.right = arg[x + 1 :]
        return ans
    return ans


def parse_cause(
    *,
    prog: str,
    warn: FunctionType,
) -> FunctionType:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_generator(
    items: list[Positional],
    *,
    abbr: Optional[Tuning],
    allowslong: bool,
    allowsshort: bool,
    expectsposix: bool,
    optNaming: HoldNaming,
    prog: str,
    warn: FunctionType,
) -> Generator[Any, Any, Any]:
    broken: bool
    cause: FunctionType
    last: Optional[Option]
    item: Positional
    broken = not (allowslong or allowsshort)
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
            abbr=abbr,
            allowslong=allowslong,
            allowsshort=allowsshort,
            cause=cause,
            optNaming=optNaming,
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


def parse_long(
    arg: str,
    *,
    abbr: Optional[Tuning],
    allowsshort: bool,
    cause: FunctionType,
    optNaming: HoldNaming,
) -> Long:
    ans: Long
    parts: list[str]
    parts = arg.split("=", 1)
    ans = Long(fullkey=parts.pop(0))
    if len(parts):
        ans.joined = True
        ans.right = parts.pop()
    ans.abbrlen = len(ans.fullkey)
    if ans.fullkey in optNaming.keys():
        parts = [ans.fullkey]
    elif abbr is not None:
        parts = parse_long_startswith(ans.abbr, keys=optNaming.keys())
    else:
        parts = list()  # can be assumed
    if len(parts) == 0:
        ans.nargs = Nargs.OPTIONAL_ARGUMENT
        cause(PIOW, option=arg, islong=True)
        return ans
    if len(parts) >= 2:
        ans.nargs = Nargs.OPTIONAL_ARGUMENT
        cause(PAOW, option=arg, possibilities=parts)
        return ans
    (ans.fullkey,) = parts
    if abbr == Tuning.MINIMIZE:
        ans.abbrlen = len(ans.fullkey)
    if abbr == Tuning.MAXIMIZE:
        parts = list(optNaming.keys())
        parts.remove(ans.fullkey)
        ans.abbrlen = parse_minlen(
            abbr=ans.abbr,
            allowsshort=allowsshort,
            joined=ans.joined,
            keys=tuple(parts),
        )
    ans.nargs = optNaming[ans.fullkey]
    if (ans.nargs == Nargs.NO_ARGUMENT) and (ans.right is not None):
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


def parse_minlen(
    *,
    abbr: str,
    allowsshort: bool,
    joined: bool,
    keys: tuple[str, ...],
) -> int:
    m: int
    n: int
    m = 2 + allowsshort - joined
    n = len(abbr)
    while n >= m and not any(z.startswith(abbr[:n]) for z in keys):
        n -= 1
    return n + 1


def parse_option(
    arg: str,
    *,
    abbr: Optional[Tuning],
    allowslong: bool,
    allowsshort: bool,
    cause: FunctionType,
    optNaming: HoldNaming,
) -> Option:
    if (allowslong and arg.startswith("--")) or not allowsshort:
        return parse_long(
            arg,
            abbr=abbr,
            allowsshort=allowsshort,
            cause=cause,
            optNaming=optNaming,
        )
    else:
        return parse_bundling(
            arg,
            cause=cause,
            optNaming=optNaming,
        )

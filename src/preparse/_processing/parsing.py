from types import FunctionType
from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["parse"]

PAOW = PreparseAmbiguousOptionWarning
PIOW = PreparseInvalidOptionWarning
PUAW = PreparseUnallowedArgumentWarning
PUOW = PreparseUnrecognizedOptionWarning
PLORAW = PreparseLongOptionRequiresArgumentWarning
PSORAW = PreparseShortOptionRequiresArgumentWarning


def parse(args: list[str], **kwargs: Any) -> list[Item]:
    return list(parse_generator(args, **kwargs))


def parse_generator(
    items: list[Positional],
    *,
    allowslong: bool,
    allowsshort: bool,
    expectsabbr: bool,
    expectsposix: bool,
    optdict: dict,
    prog: str,
    warn: FunctionType,
) -> Generator[Any, Any, Any]:
    broken: bool = not (allowslong or allowsshort)
    cause: FunctionType = parse_cause(prog=prog, warn=warn)
    last: Optional[Option] = None
    item: Positional
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
            allowslong=allowslong,
            allowsshort=allowsshort,
            cause=cause,
            expectsabbr=expectsabbr,
            optdict=optdict,
        )
        if not last.ishungry():
            yield last
            last = None
    if last is None:
        # if the last item is not starved
        return
    if isinstance(last, Long):
        cause(PLORAW, option=last.fullkey)
    else:
        cause(PSORAW, option=last.chars[-1])
    yield last


def parse_cause(
    *,
    prog: str,
    warn: FunctionType,
) -> FunctionType:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_option(
    arg: str,
    *,
    cause: FunctionType,
    expectsabbr: bool,
    optdict: dict,
    **kwargs: Any,
) -> Option:
    if parse_islong(arg, **kwargs):
        return parse_long(
            arg,
            cause=cause,
            expectsabbr=expectsabbr,
            optdict=optdict,
        )
    else:
        return parse_bundling(
            arg,
            cause=cause,
            optdict=optdict,
        )


def parse_islong(
    arg: str,
    *,
    allowslong: bool,
    allowsshort: bool,
) -> bool:
    if allowslong and allowsshort:
        return arg.startswith("--")
    else:
        return not allowsshort


def parse_long(
    arg: str,
    *,
    cause: FunctionType,
    expectsabbr: bool,
    optdict: dict,
) -> Long:
    parts: list[str] = arg.split("=", 1)
    ans: Long = Long(fullkey=parts.pop(0))
    ans.abbrlen = len(ans.fullkey)
    if len(parts):
        ans.joined = True
        ans.right = parts.pop()
    ans.fullkey = parse_long_full(
        ans,
        cause=cause,
        expectsabbr=expectsabbr,
        keys=list(optdict.keys()),
    )
    try:
        ans.nargs = optdict[ans.fullkey]
    except KeyError:
        ans.nargs = Nargs.OPTIONAL_ARGUMENT
        cause(PUOW, option=arg)
        return ans
    if (ans.nargs == Nargs.NO_ARGUMENT) and (ans.right is not None):
        cause(PUAW, option=ans.fullkey)
    return ans


def parse_long_full(
    item: Long,
    *,
    cause: FunctionType,
    expectsabbr: bool,
    keys: list[str],
) -> str:
    if item.fullkey in keys:
        return item.fullkey
    if not expectsabbr:
        cause(PUOW, option=arg)
    x: str
    pos: list[str] = list()
    for x in keys:
        if x.startswith(item.fullkey):
            pos.append(x)
    if len(pos) == 1:
        return pos[0]
    arg: str = item.fullkey
    if item.joined:
        arg += "=" + item.right
    if len(pos) == 0:
        cause(PUOW, option=arg)
    else:
        cause(PAOW, option=arg, possibilities=pos)
    return item.fullkey


def parse_bundling(
    arg: str,
    *,
    cause: FunctionType,
    optdict: dict,
) -> Bundle:
    ans: Bundle = Bundle(chars="")
    for i, a in enumerate(arg):
        if i == 0:
            continue
        ans.chars += a
        try:
            ans.nargs = optdict["-" + a]
        except KeyError:
            cause(PIOW, option=a)
            ans.nargs = Nargs.NO_ARGUMENT
        if ans.nargs == Nargs.NO_ARGUMENT:
            continue
        if ans.nargs == Nargs.OPTIONAL_ARGUMENT or i < len(arg) - 1:
            ans.joined = True
            ans.right = arg[i + 1 :]
        return ans
    return ans

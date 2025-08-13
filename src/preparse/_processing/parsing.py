from types import FunctionType
from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["parse"]

PUOW = PreparseUnrecognizedOptionWarning
PAOW = PreparseAmbiguousOptionWarning
PUAW = PreparseUnallowedArgumentWarning
PIOW = PreparseInvalidOptionWarning
PLORAW = PreparseLongOptionRequiresArgumentWarning
PSORAW = PreparseShortOptionRequiresArgumentWarning


def parse(args: list[str], **kwargs) -> list[Item]:
    return list(parse_generator(args, **kwargs))


def parse_generator(
    items: list[Positional],
    *,
    optdict: dict,
    expectsabbr: bool,
    expandsabbr: bool,
    expectsposix: bool,
    prog: str,
    warn: FunctionType,
    allowslong: bool,
    allowsshort: bool,
) -> Generator[Any, Any, Any]:
    if not allowslong:
        raise NotImplementedError
    cause: FunctionType = parse_cause(prog=prog, warn=warn)
    broken: bool = False
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
        if item.value.startswith("--") or not allowsshort:
            last = parse_long(
                item.value,
                cause=cause,
                optdict=optdict,
                expectsabbr=expectsabbr,
                expandsabbr=expandsabbr,
            )
        else:
            last = parse_bundling(item.value, optdict=optdict, cause=cause)
        if not last.ishungry():
            yield last
            last = None
    if last is None:
        # if the last item is not starved
        return
    if isinstance(last.joined, str):
        cause(PLORAW, option=last.joined)
        last.joined = True
    else:
        cause(PSORAW, option=last.chars[-1])
    yield last


def parse_cause(*, prog: str, warn: FunctionType) -> FunctionType:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_long(
    arg: str,
    *,
    cause: FunctionType,
    optdict: dict,
    expectsabbr: bool,
    expandsabbr: bool,
) -> Long:
    ans: Long = parse_long_init(arg)
    full: str = parse_long_full(
        ans,
        cause=cause,
        keys=list(optdict.keys()),
        expectsabbr=expectsabbr,
    )
    nargs: Nargs = optdict.get(full, Nargs.NO_ARGUMENT)
    if nargs == Nargs.NO_ARGUMENT and ans.joined:
        cause(PUAW, option=full)
    if nargs == Nargs.REQUIRED_ARGUMENT:
        ans.joined = True
    if ans.joined:
        ans.joined = full
    if expandsabbr:
        ans.left = full
    return ans


def parse_long_init(arg: str) -> Long:
    parts: list[str] = arg.split("=", 1)
    ans: Long = Long(left=parts.pop(0))
    if len(parts):
        ans.joined = True
        ans.right = parts.pop()
    return ans


def parse_long_full(
    item: Long, *, cause: FunctionType, keys: list[str], expectsabbr: bool
) -> str:
    if item.left in keys:
        return item.left
    if not expectsabbr:
        cause(PUOW, option=arg)
    x: str
    pos: list[str] = list()
    for x in keys:
        if x.startswith(item.left):
            pos.append(x)
    if len(pos) == 1:
        return pos[0]
    arg: str = item.left
    if item.joined:
        arg += "=" + item.right
    if len(pos) == 0:
        cause(PUOW, option=arg)
    else:
        cause(PAOW, option=arg, possibilities=pos)
    return item.left


def parse_bundling(arg: str, **kwargs: Any) -> Bundle:
    ans: Bundle = Bundle(chars="")
    nargs: Nargs
    for i, a in enumerate(arg):
        if i == 0:
            continue
        ans.chars += a
        nargs = parse_bundling_letter(a, **kwargs)
        if nargs == Nargs.NO_ARGUMENT:
            continue
        if nargs == Nargs.OPTIONAL_ARGUMENT or i < len(arg) - 1:
            ans.joined = True
            ans.right = arg[i + 1 :]
        else:
            ans.joined = nargs == Nargs.REQUIRED_ARGUMENT
        return ans
    return ans


def parse_bundling_letter(letter: str, *, optdict: dict, cause: FunctionType) -> Nargs:
    try:
        return optdict["-" + letter]
    except KeyError:
        cause(PIOW, option=letter)
        return Nargs.NO_ARGUMENT

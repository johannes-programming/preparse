from types import FunctionType
from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser
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
    args: list[str], *, parser: "PreParser"
) -> Generator[Any, Any, Any]:
    if not parser.allowslong:
        raise NotImplementedError
    cause: FunctionType = parse_cause(prog=parser.prog, warn=parser.warn)
    broken: bool = False
    last: Optional[Item] = None
    for arg in args:
        if broken:
            # if we are in the positional-only part
            yield Item(value=arg)
            continue
        if last is not None:
            # if the last item hungers for a value
            last.value = arg
            last.remainder = False
            yield last
            last = None
            continue
        if arg == "--":
            yield Item()
            broken = True
            continue
        if arg == "-" or not arg.startswith("-"):
            # if the arg is positional
            yield Item(value=arg)
            broken = parser.expectsposix
            continue
        if arg.startswith("--") or not parser.allowsshort:
            last = parse_long(arg, parser=parser, cause=cause)
        else:
            last = parse_bundling(arg, optdict=parser.optdict, cause=cause)
        if not last.ishungry():
            yield last
            last = None
    if last is None:
        # if the last item is not starved
        return
    if isinstance(last.remainder, str):
        cause(PLORAW, option=last.remainder)
        last.remainder = True
    else:
        cause(PSORAW, option=last.key[-1])
    yield last


def parse_cause(*, prog: str, warn: FunctionType) -> FunctionType:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_long(arg: str, *, parser: "PreParser", cause: FunctionType) -> Item:
    ans: Item = parse_long_init(arg)
    full: str = parse_long_full(ans, parser=parser, cause=cause)
    nargs: Nargs = parser.optdict.get(full, Nargs.NO_ARGUMENT)
    if nargs == Nargs.NO_ARGUMENT and ans.remainder:
        cause(PUAW, option=full)
    if nargs == Nargs.REQUIRED_ARGUMENT:
        ans.remainder = True
    if ans.remainder:
        ans.remainder = full
    if parser.expandsabbr:
        ans.key = full
    return ans


def parse_long_init(arg: str) -> Item:
    if "=" not in arg:
        return Item(key=arg)
    ans: Item = Item(remainder=True)
    ans.key, ans.value = arg.split("=", 1)
    return ans


def parse_long_full(item: Item, *, parser: "PreParser", cause: FunctionType) -> str:
    if item.key in parser.optdict.keys():
        return item.key
    if not parser.expectsabbr:
        cause(PUOW, option=arg)
    x: str
    pos: list[str] = list()
    for x in parser.optdict.keys():
        if x.startswith(item.key):
            pos.append(x)
    if len(pos) == 1:
        return pos[0]
    arg: str = item.key
    if item.remainder:
        arg += "=" + item.value
    if len(pos) == 0:
        cause(PUOW, option=arg)
    else:
        cause(PAOW, option=arg, possibilities=pos)
    return item.key


def parse_bundling(arg: str, **kwargs: Any) -> Item:
    ans: Item = Item(key="")
    nargs: Nargs
    for i, a in enumerate(arg):
        if i == 0:
            continue
        ans.key += a
        nargs = parse_bundling_letter(a, **kwargs)
        if nargs == Nargs.NO_ARGUMENT:
            continue
        if nargs == Nargs.OPTIONAL_ARGUMENT or i < len(arg) - 1:
            ans.remainder = True
            ans.value = arg[i + 1 :]
        else:
            ans.remainder = nargs == Nargs.REQUIRED_ARGUMENT
        return ans
    return ans


def parse_bundling_letter(letter: str, *, optdict: dict, cause: FunctionType) -> Nargs:
    try:
        return optdict["-" + letter]
    except KeyError:
        cause(PIOW, option=letter)
        return Nargs.NO_ARGUMENT

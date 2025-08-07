from typing import *

from preparse._parsing.Item import *
from preparse.core.enums import *
from preparse.core.warnings import *
import dataclasses
import types

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser
__all__ = ["parse"]

PUOW = PreparseUnrecognizedOptionWarning
PAOW = PreparseAmbiguousOptionWarning
PUAW = PreparseUnallowedArgumentWarning
PIOW = PreparseInvalidOptionWarning
PLORAW = PreparseLongOptionRequiresArgumentWarning
PSORAW = PreparseShortOptionRequiresArgumentWarning

def parse(
    args:Optional[Iterable],*,
    cause_warning=types.MethodType,
    islongonly:bool, 
    isposix:bool, 
    optdict:dict[str,Nargs], 
    rejectabbr:bool,
) -> Generator[Item, None, None]:
    broken: bool = False
    last: Optional[Item] = None
    for arg in args:
        if broken:
            # if we are in the positional-only part
            yield Item(right=arg)
            continue
        if last is not None:
            # if the last item hungers for a value
            last.right = arg
            yield last
            last = None
            continue
        if arg == "--":
            yield Item()
            broken = True
            continue
        if arg == "-" or not arg.startswith("-"):
            # if the arg is positional
            yield Item(right=arg)
            broken = isposix
            continue
        if arg.startswith("--") or islongonly:
            return parse_long(arg=arg, optdict=optdict, )
        else:
            return parse_group(arg=arg, **kwargs)
        last = parse_option(
            arg=arg, 
            islongonly=islongonly,
            optdict=optdict, 
            warnUtil=warnUtil,
        )
        if not last.ishungry():
            yield last
            last = None
    if last is None:
        # if the last item is not starved
        return
    if isinstance(last.joined, str):
        warnUtil(PLORAW, option=last.joined)
    else:
        warnUtil(PSORAW, option=last.key[-1])
        parser.warn(warning)
    yield last


def parse_option(arg:str, *, islongonly:bool, **kwargs:Any)->Item:
    if arg.startswith("--") or islongonly:
        return parse_long(arg=arg, **kwargs)
    else:
        return parse_group(arg=arg, **kwargs)


def parse_long(*, arg: str, parser: "PreParser") -> Item:
    ans: Item = parse_long_init(arg)
    full: str = parse_long_full(item=ans, parser=parser)
    nargs: Nargs = parser.optdict.get(full, Nargs.NO_ARGUMENT)
    if nargs == Nargs.NO_ARGUMENT and ans.joined:
        warning = PUAW(prog=parser.prog, option=full)
        parser.warn(warning)
    if nargs == Nargs.REQUIRED_ARGUMENT:
        ans.joined = True
    if ans.joined:
        ans.joined = full
    if parser.abbr == Abbr.COMPLETE:
        ans.key = full
    return ans


def parse_long_init(arg: str) -> Item:
    if "=" not in arg:
        return Item(key=arg)
    ans: Item = Item(joined=True)
    ans.key, ans.right = arg.split("=", 1)
    return ans


def parse_long_full(*, item: Item, parser: "PreParser") -> str:
    if item.key in parser.optdict.keys():
        return item.key
    if parser.abbr == Abbr.REJECT:
        warning: PUOW = PUOW(prog=parser.prog, option=arg)
        parser.warn(warning)
    x: str
    pos: list[str] = list()
    for x in parser.optdict.keys():
        if x.startswith(item.key):
            pos.append(x)
    if len(pos) == 1:
        return pos[0]
    arg: str = item.key
    if item.joined:
        arg += "=" + item.right
    if len(pos) == 0:
        warning: PUOW = PUOW(prog=parser.prog, option=arg)
        parser.warn(warning)
    else:
        warning: PAOW = PAOW(prog=parser.prog, option=arg, possibilities=pos)
        parser.warn(warning)
    return item.key


def parse_group_letter(letter: str, *, parser: "PreParser") -> Nargs:
    try:
        return parser.optdict["-" + letter]
    except KeyError:
        warning: PIOW = PIOW(prog=parser.prog, option=letter)
        parser.warn(warning)
        return Nargs.NO_ARGUMENT


def parse_group(*, arg: str, parser: "PreParser") -> Item:
    ans: Item = Item(key="")
    nargs: Nargs
    for i, a in enumerate(arg):
        if i == 0:
            continue
        ans.key += a
        nargs = parse_group_letter(a, parser=parser)
        if nargs == Nargs.NO_ARGUMENT:
            continue
        if nargs == Nargs.OPTIONAL_ARGUMENT or i < len(arg) - 1:
            ans.joined = True
            ans.right = arg[i + 1 :]
        else:
            ans.joined = nargs == Nargs.REQUIRED_ARGUMENT
        return ans
    return ans

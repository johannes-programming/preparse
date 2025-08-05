
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *
from preparse._parsing.Item import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["deparse"]

def deparse(items:list[Item])->list:
    ans:list[str]=list()
    item:Item
    for item in items:
        if item.isspecial():
            ans.append("--")
        if item.ispositional():
            ans.append(item.value)
        if item.islong():
            







def get_long_possibilities(*, trunk:str, parser:"PreParser")->list:
    if trunk in parser.optdict.keys():
        return [trunk]
    if parser.abbr == Abbr.REJECT:
        return list()
    ans: list = list()
    for k in parser.optdict.keys():
        if k.startswith(trunk):
            ans.append(k)
    return ans

def get_nargs_for_letter(*, parser:"PreParser", letter: str) -> Nargs:
    try:
        return parser.optdict["-" + letter]
    except KeyError:
        warn(
            PreparseInvalidOptionWarning,
            parser=parser,
            option=letter,
        )
        return Nargs.NO_ARGUMENT
    
def is_certainly_not_an_option(arg:str)->bool:
    return arg=="-" or not arg.startswith("-")

def parse(args:list[str], /, *, parser:"PreParser"):
    last:Optional[Item] = None
    broken:bool = False
    for a in args:
        if broken:
            yield Item(value=a)
            continue
        if last is not None:
            last.value = a
            yield last
            last = None
            continue
        if a == "--":
            yield Item()
            broken = True
            continue
        if is_certainly_not_an_option(a):
            yield Item(value=a)
            broken = parser.order == Order.POSIX
            continue
        last = reflect(arg=a, parser=parser)
        if last.equal and last.value is None:
            last.equal = False
        else:
            yield last
            last = None
    if last is not None:
        yield last


def reflect(arg:str, *, parser:"PreParser"):
    if arg.startswith("--") or parser.longonly:
        return reflect_long(arg, parser=parser)
    else:
        return reflect_short(arg, parser=parser)

def reflect_short(arg:str, *, parser:"PreParser"):
    item=Item(key="")

    i:int
    a:str
    nargs:Nargs
    for i, a in enumerate(arg):
        if i == 0:
            continue
        nargs = get_nargs_for_letter(parser=parser, letter=a)
        if nargs == Nargs.NO_ARGUMENT:
            item.key+=a
            continue
        if i + 1 < len(arg):
            item.equal = True
            item.value = arg[i + 1 :]
        else:
            item.equal = nargs == Nargs.REQUIRED_ARGUMENT
        return item
    return item

def reflect_long(arg:str, *, item:Item, parser:"PreParser"):
    item = Item()
    item.equal = "=" in arg
    if item.equal:
        item.comment, item.value = arg.split("=", 1)
    else:
        item.comment = arg
    pos:list = get_long_possibilities(trunk=item.comment, parser=parser)
    if len(pos) == 0:
        warn(
            PreparseUnrecognizedOptionWarning,
            parser=parser,
            option=arg,
        )
        item.key = item.comment
        return item
    if len(pos) > 1:
        warn(
            PreparseAmbiguousOptionWarning,
            parser=parser,
            option=arg,
            possibilities=pos,
        )
        item.key = item.comment
        return item
    item.key = pos[0]
    if item.value is None:
        item.equal = parser.optdict[item.key] == Nargs.REQUIRED_ARGUMENT
    elif parser.optdict[item.key] == Nargs.NO_ARGUMENT:
        warn(
            PreparseUnallowedArgumentWarning,
            parser=parser,
            option=item.key,
        )
    return item
    
def warn(wrncls: type, /, *, parser:"PreParser",  **kwargs: Any) -> None:
    parser.warn(wrncls(prog=parser.prog, **kwargs))


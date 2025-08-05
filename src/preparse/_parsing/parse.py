
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *
from preparse._parsing.Item import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["parse"]


def get_initial_long_item(arg:str)->Item:
    ans:Item = Item(equal="=" in arg)
    if ans.equal:
        ans.key, ans.value = arg.split("=", 1)
    else:
        ans.key = arg
    return ans

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
        warn(PIOW, parser=parser, option=letter)
        return Nargs.NO_ARGUMENT


def parse(args:list[str], /, *, parser:"PreParser"):
    last:Optional[Item] = None
    broken:bool = False
    for a in args:
        if broken:
            yield Item(value=a)
            continue
        if last is not None:
            last.value = a
            last.equal = parser.remainder == Remainder.MAXIMIZE
            yield last
            last = None
            continue
        if a == "--":
            yield Item()
            broken = True
            continue
        if a=="-" or not a.startswith("-"):
            yield Item(value=a)
            broken = parser.order == Order.POSIX
            continue
        last = reflect(arg=a, parser=parser)
        if not last.isstarving():
            yield last
            last = None
    if last is not None:
        yield last


def reflect(arg:str, *, parser:"PreParser")->Item:
    if arg.startswith("--") or parser.longonly:
        return reflect_long(arg, parser=parser)
    else:
        return reflect_short(arg, parser=parser)

def reflect_short(arg:str, *, parser:"PreParser"):
    nargs:Nargs = Nargs.NO_ARGUMENT
    i:int = 0
    while nargs == Nargs.NO_ARGUMENT:
        i += 1
        if i == len(arg):
            return Item(key=arg[1:])
        nargs = get_nargs_for_letter(parser=parser, letter=arg[i])
    ans:Item = Item()
    ans.key=arg[1:i+1]
    if i + 1 < len(arg):
        # if there is a value
        ans.value = arg[i + 1:]
        ans.equal = nargs != Nargs.REQUIRED_ARGUMENT or parser.remainder != Remainder.MINIMIZE
    else:
        # if there is no value
        # but one is required
        # then make the item starving
        ans.equal = nargs == Nargs.REQUIRED_ARGUMENT
    return ans

def reflect_long(arg:str, *, item:Item, parser:"PreParser"):
    # get initial information
    item :Item= get_initial_long_item(arg)
    pos:list[str] = get_long_possibilities(trunk=item.key, parser=parser)
    # determine nargs
    nargs:Nargs
    if len(pos) == 0:
        warn(PUOW, parser=parser, option=arg)
        nargs = Nargs.NO_ARGUMENT
    elif len(pos) == 1:
        nargs = parser.optdict[pos[0]]
        if parser.abbr == Abbr.COMPLETE:
            item.key = pos[0]
    else:
        warn(PAOW, parser=parser, option=arg, possibilities=pos)
        nargs = Nargs.NO_ARGUMENT
    # put the pieces together
    if nargs == Nargs.REQUIRED_ARGUMENT:
        item.equal = item.value is None or parser.remainder != Remainder.MINIMIZE
    if nargs == Nargs.NO_ARGUMENT:
        if item.value is not None:
            warn(PUAW, parser=parser,option=item.key)
    return item
    
def warn(wrncls: type, /, *, parser:"PreParser",  **kwargs: Any) -> None:
    parser.warn(wrncls(prog=parser.prog, **kwargs))


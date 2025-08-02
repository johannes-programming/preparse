
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *
from preparse._parsing.Item import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["preparse"]

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
        last = Item()
        if reflect(item=last, arg=a, parser=parser):
            yield last
            last = None

def reflect(arg:str, *, item:Item, parser:Any):
    if not arg.startswith("--"):
        return reflect_short(arg, item=item, parser=parser)
    else:
        return reflect_long(*arg.split("=", 1), item=item, parser=parser)
            

def reflect_long(trunk:str, value:Optional[str]=None, *, item:Item, parser:Any):
    item.key = get_long_key(trunk=trunk, parser=parser)
    item.equal = True
    item.value = value
    item.comment = trunk
    if 
    
    



    optn = self.tick(optn)
    self.lasttick(optn)
    self.dumpspec()

    def dumpspec(self: Self) -> None:
        self.ans.extend(self.spec)
        self.spec.clear()

    def get_nargs_for_letter(self: Self, letter: str) -> Nargs:
        try:
            return self.optdict["-" + letter]
        except KeyError:
            self.warn(
                PreparseInvalidOptionWarning,
                prog=self.parser.prog,
                option=letter,
            )
            return Nargs.NO_ARGUMENT

    @functools.cached_property
    def islongonly(self: Self) -> bool:
        # if a long option with a single hyphon exists
        # then all options are treated as long options
        # example: -foo
        for k in self.optdict.keys():
            if len(k) < 3:
                continue
            if k.startswith("--"):
                continue
            if not k.startswith("-"):
                continue
            return True
        return False

    def lasttick(self: Self, optn: str) -> None:
        if optn != "open":
            return
        self.warn(
            PreparseRequiredArgumentWarning,
            prog=self.parser.prog,
            option=self.ans[-1],
        )

    @functools.cached_property
    def optdict(self: Self) -> Dict[str, Nargs]:
        ans: dict = dict()
        for k, v in self.parser.optdict.items():
            ans[str(k)] = Nargs(v)
        return ans

    def possibilities(self: Self, opt: str) -> list[str]:
        if opt in self.optdict.keys():
            return [opt]
        if self.parser.abbr == Abbr.REJECT:
            return list()
        ans: list = list()
        for k in self.optdict.keys():
            if k.startswith(opt):
                ans.append(k)
        return ans

    def tick(self: Self, optn: str) -> str:
        if optn == "break":
            # if no more options are allowed
            self.spec.extend(self.args)
            self.args.clear()
            return "break"
        arg: str = self.args.pop(0)
        if optn == "open":
            # if a value for an option is already expected
            self.ans.append(arg)
            return "closed"
        if arg == "--":
            # if arg is the special argument
            self.ans.append("--")
            return "break"
        hasgroup: bool = optn == "group"
        if arg.startswith("-") and arg != "-":
            # if arg is an option
            return self.tick_opt(arg, hasgroup=hasgroup)
        else:
            # if arg is positional
            return self.tick_pos(arg, hasgroup=hasgroup)

    def tick_opt(self: Self, arg: str, /, *, hasgroup: bool) -> str:
        if arg.startswith("--") or self.islongonly:
            return self.tick_opt_long(arg)
        else:
            return self.tick_opt_short(arg, hasgroup=hasgroup)

    def tick_opt_long(self: Self, arg: str) -> str:
        try:
            i: int = arg.index("=")
        except ValueError:
            i: int = len(arg)
        opt: str = arg[:i]
        possibilities: list = self.possibilities(opt)
        if len(possibilities) == 0:
            self.warn(
                PreparseUnrecognizedOptionWarning,
                prog=self.parser.prog,
                option=arg,
            )
            self.ans.append(arg)
            return "closed"
        if len(possibilities) > 1:
            self.warn(
                PreparseAmbiguousOptionWarning,
                prog=self.parser.prog,
                option=arg,
                possibilities=possibilities,
            )
            self.ans.append(arg)
            return "closed"
        opt = possibilities[0]
        if self.parser.abbr == Abbr.COMPLETE:
            self.ans.append(opt + arg[i:])
        else:
            self.ans.append(arg)
        if "=" in arg:
            if self.optdict[opt] == 0:
                warning = PreparseUnallowedArgumentWarning(
                    prog=self.parser.prog,
                    option=opt,
                )
                self.parser.warn(warning)
            return "closed"
        else:
            if self.optdict[opt] == 1:
                return "open"
            else:
                return "closed"

    def tick_opt_short(self: Self, arg: str, /, *, hasgroup: bool) -> str:
        i: int
        a: str
        nargs: Nargs
        if self.parser.group != Group.MINIMIZE:
            self.ans.append("-")
        if (self.parser.group == Group.MAXIMIZE) and hasgroup:
            self.ans.pop()
        for i, a in enumerate(arg):
            if i == 0:
                continue
            if self.parser.group != Group.MINIMIZE:
                self.ans[-1] += a
            elif a == "-":
                self.ans[-1] += a
            else:
                self.ans.append("-" + a)
            nargs = self.get_nargs_for_letter(a)
            if nargs == Nargs.NO_ARGUMENT:
                continue
            value: str = arg[i + 1 :]
            return self.tick_opt_short_nongroup(nargs=nargs, value=value)
        return "group"

    def tick_opt_short_nongroup(self: Self, *, nargs: Nargs, value: str) -> str:
        if value:
            self.ans[-1] += value
            return "closed"
        if nargs == Nargs.OPTIONAL_ARGUMENT:
            return "closed"
        return "open"

    def tick_pos(self: Self, arg: str, *, hasgroup: bool) -> str:
        self.spec.append(arg)
        if self.parser.order == Order.POSIX:
            return "break"
        elif self.parser.order == Order.GIVEN:
            self.dumpspec()
            return "closed"
        else:
            return "group" if hasgroup else "closed"

    def warn(self: Self, wrncls: type, /, **kwargs: Any) -> None:
        wrn: PreparseWarning = wrncls(**kwargs)
        self.parser.warn(wrn)

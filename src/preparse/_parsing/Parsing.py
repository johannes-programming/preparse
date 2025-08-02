import dataclasses
import functools
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["Parsing"]


@dataclasses.dataclass
class Parsing:
    parser: "PreParser"
    args: list[str]

    def __post_init__(self: Self) -> None:
        self.ans = list()
        self.spec = list()
        optn: str = "seal"
        while self.args:
            optn = self.tick(optn)
        self.lasttick(optn)
        self.dumpspec()

    def dumpspec(self: Self) -> None:
        self.ans.extend(self.spec)
        self.spec.clear()


    def get_nargs_for_option_letter(self:Self, letter:str) -> Nargs:
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
        if optn != "grab":
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
        if optn == "grab":
            # if a value for an option is already expected
            self.ans.append(arg)
            return "seal"
        if arg == "--":
            # if arg is the special argument
            self.ans.append("--")
            return "break"
        if arg.startswith("-") and arg != "-":
            # if arg is an option
            return self.tick_opt(arg, isgroup=optn=="group")
        else:
            # if arg is positional
            return self.tick_pos(arg)

    def tick_opt(self: Self, arg: str, *,isgroup:bool) -> str:
        if arg.startswith("--") or self.islongonly:
            return self.tick_opt_long(arg)
        else:
            return self.tick_opt_short(arg, isgroup=isgroup)

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
            return "seal"
        if len(possibilities) > 1:
            self.warn(
                PreparseAmbiguousOptionWarning,
                prog=self.parser.prog,
                option=arg,
                possibilities=possibilities,
            )
            self.ans.append(arg)
            return "seal"
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
            return "seal"
        else:
            if self.optdict[opt] == 1:
                return "grab"
            else:
                return "seal"
        
    def tick_opt_short(self: Self, arg: str, *, isgroup:bool) -> str:
        if self.parser.group == Group.MINIMIZE:
            return self.tick_opt_short_min(arg)
        else:
            return self.tick_opt_short_nonmin(arg, isgroup=isgroup)


    def tick_opt_short_min(self: Self, arg: str) -> str:
        i:int
        a:str
        nargs :Nargs
        for i, a in enumerate(arg):
            if i == 0:
                continue
            if a == "-":
                self.ans[-1] += a
            else:
                self.ans.append("-" + a)
            nargs = self.get_nargs_for_option_letter(a)
            if nargs == Nargs.NO_ARGUMENT:
                continue
            value = arg[i+1:]
            if value:
                self.ans[-1] += value
                return "seal"
            if nargs != Nargs.REQUIRED_ARGUMENT:
                return "seal"
            return "grab"
        return "seal"
        
    def tick_opt_short_nonmin(self: Self, arg: str, *,isgroup:bool) -> str:
        if isgroup and self.parser.group == Group.MAXIMIZE:
            self.ans[-1] += arg[1:]
        else:
            self.ans.append(arg)
        i:int
        a:str
        nargs : Nargs 
        for i, a in enumerate(arg):
            if i == 0:
                continue
            nargs = self.get_nargs_for_option_letter(a)
            if nargs != Nargs.NO_ARGUMENT:
                break
            value = arg[i + 1:]
            if value:
                return "seal"
            if nargs != Nargs.REQUIRED_ARGUMENT:
                return "seal"
            return "grab"
        return "group"
        
    def tick_opt_short_maintain(self: Self, arg: str) -> str:
        self.ans.append(arg)
        nargs = 0
        for i, a in enumerate(arg):
            if i == 0:
                continue
            if nargs != 0:
                return "seal"
            nargs = self.get_nargs_for_option_letter(a)
        if nargs == 1:
            return "grab"
        else:
            return "seal"

    def tick_pos(self: Self, arg: str) -> str:
        self.spec.append(arg)
        if self.parser.order == Order.POSIX:
            return "break"
        elif self.parser.order == Order.GIVEN:
            self.dumpspec()
            return "seal"
        else:
            return "seal"

    def warn(self: Self, wrncls: type, /, **kwargs: Any) -> None:
        wrn: PreparseWarning = wrncls(**kwargs)
        self.parser.warn(wrn)

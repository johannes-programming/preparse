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
        optn: str = "closed"
        while self.args:
            optn = self.tick(optn)
        self.lasttick(optn)
        self.dumpspec()

    def dumpspec(self: Self) -> None:
        self.ans.extend(self.spec)
        self.spec.clear()

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
        if arg.startswith("-") and arg != "-":
            # if arg is an option
            return self.tick_opt(arg)
        else:
            # if arg is positional
            return self.tick_pos(arg)

    def tick_opt(self: Self, arg: str) -> str:
        if arg.startswith("--") or self.islongonly:
            return self.tick_opt_long(arg)
        else:
            return self.tick_opt_short(arg)

    def tick_opt_long(self: Self, arg: str) -> str:
        if "=" in arg:
            return self.tick_opt_long_eq(arg)
        else:
            return self.tick_opt_long_ne(arg)
            
    def tick_opt_long_eq(self: Self, arg: str) -> str:
        opt:str = ""
        value:str = ""
        opt, value = arg.split("=", 1)
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
            self.ans.append(opt + "=" + value)
        else:
            self.ans.append(arg)
        if self.optdict[opt] == 0:
            warning = PreparseUnallowedArgumentWarning(
                prog=self.parser.prog,
                option=opt,
            )
            self.parser.warn(warning)
        return "closed"
            
    def tick_opt_long_ne(self: Self, arg: str) -> str:
        pos: list = self.possibilities(arg)
        if len(pos) == 0:
            self.warn(
                PreparseUnrecognizedOptionWarning,
                prog=self.parser.prog,
                option=arg,
            )
            self.ans.append(arg)
            return "closed"
        if len(pos) > 1:
            self.warn(
                PreparseAmbiguousOptionWarning,
                prog=self.parser.prog,
                option=arg,
                possibilities=pos,
            )
            self.ans.append(arg)
            return "closed"
        if self.parser.abbr == Abbr.COMPLETE:
            self.ans.append(pos[0])
        else:
            self.ans.append(arg)
        if self.optdict[pos[0]] == 1:
            return "open"
        else:
            return "closed"

    def tick_opt_short(self: Self, arg: str) -> str:
        self.ans.append(arg)
        nargs = 0
        for i in range(1 - len(arg), 0):
            if nargs != 0:
                return "closed"
            nargs = self.optdict.get("-" + arg[i])
            if nargs is None:
                warning = PreparseInvalidOptionWarning(
                    prog=self.parser.prog,
                    option=arg[i],
                )
                self.parser.warn(warning)
                nargs = 0
        if nargs == 1:
            return "open"
        else:
            return "closed"

    def tick_pos(self: Self, arg: str) -> str:
        self.spec.append(arg)
        if self.parser.order == Order.POSIX:
            return "break"
        elif self.parser.order == Order.GIVEN:
            self.dumpspec()
            return "closed"
        else:
            return "closed"

    def warn(self: Self, wrncls: type, /, **kwargs: Any) -> None:
        wrn: PreparseWarning = wrncls(**kwargs)
        self.parser.warn(wrn)

import dataclasses
import functools
from typing import *

from preparse.core.enums import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["Parsing"]


@dataclasses.dataclass
class Parsing:
    parser: "PreParser"
    args: list[str]

    def __post_init__(self) -> None:
        self.ans = list()
        self.spec = list()
        optn = "closed"
        while self.args:
            optn = self.tick(optn)
        self.lasttick(optn)
        self.dumpspec()

    def dumpspec(self) -> None:
        self.ans.extend(self.spec)
        self.spec.clear()

    @functools.cached_property
    def islongonly(self) -> bool:
        for k in self.optdict.keys():
            if len(k) < 3:
                continue
            if k.startswith("--"):
                continue
            if not k.startswith("-"):
                continue
            # example: -foo
            return True
        return False

    def lasttick(self, optn: str) -> None:
        if optn != "open":
            return
        self.parser.warnAboutRequiredArgument(self.ans[-1])

    @functools.cached_property
    def optdict(self) -> Dict[str, Nargs]:
        ans = dict()
        for k, v in self.parser.optdict.items():
            ans[str(k)] = Nargs(v)
        return ans

    def possibilities(self, opt: str) -> list[str]:
        if opt in self.optdict.keys():
            return [opt]
        if self.parser.longOptionAbbreviations == LongOptionAbbreviations.REJECT:
            return list()
        ans = list()
        for k in self.optdict.keys():
            if k.startswith(opt):
                ans.append(k)
        return ans

    def tick(self, optn: str) -> str:
        if optn == "break":
            self.spec.extend(self.args)
            self.args.clear()
            return "break"
        arg = self.args.pop(0)
        if optn == "open":
            self.ans.append(arg)
            return "closed"
        if arg == "--":
            self.ans.append("--")
            return "break"
        if arg.startswith("-") and arg != "-":
            return self.tick_opt(arg)
        else:
            return self.tick_pos(arg)

    def tick_opt(self, arg: str) -> str:
        if arg.startswith("--") or self.islongonly:
            return self.tick_opt_long(arg)
        else:
            return self.tick_opt_short(arg)

    def tick_opt_long(self, arg: str) -> str:
        try:
            i = arg.index("=")
        except ValueError:
            i = len(arg)
        opt = arg[:i]
        possibilities = self.possibilities(opt)
        if len(possibilities) == 0:
            self.parser.warnAboutUnrecognizedOption(arg)
            self.ans.append(arg)
            return "closed"
        if len(possibilities) > 1:
            self.parser.warnAboutAmbiguousOption(arg, possibilities)
            self.ans.append(arg)
            return "closed"
        opt = possibilities[0]
        if self.parser.longOptionAbbreviations == LongOptionAbbreviations.COMPLETE:
            self.ans.append(opt + arg[i:])
        else:
            self.ans.append(arg)
        if "=" in arg:
            if self.optdict[opt] == 0:
                self.parser.warnAboutUnallowedArgument(opt)
            return "closed"
        else:
            if self.optdict[opt] == 1:
                return "open"
            else:
                return "closed"

    def tick_opt_short(self, arg: str) -> str:
        self.ans.append(arg)
        nargs = 0
        for i in range(1 - len(arg), 0):
            if nargs != 0:
                return "closed"
            nargs = self.optdict.get("-" + arg[i])
            if nargs is None:
                self.parser.warnAboutInvalidOption(arg[i])
                nargs = 0
        if nargs == 1:
            return "open"
        else:
            return "closed"

    def tick_pos(self, arg: str) -> str:
        self.spec.append(arg)
        if self.parser.posix:
            return "break"
        elif self.parser.permutate:
            return "closed"
        else:
            self.dumpspec()
            return "closed"

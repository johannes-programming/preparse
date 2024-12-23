import dataclasses
import enum
import functools
import os
import sys
import types
import warnings
from typing import *

import click as cl
from datarepr import datarepr
from makeprop import makeprop

__all__ = ["Abbrev", "Click", "Nargs", "PreParser"]


class Abbrev(enum.IntEnum):
    REJECT = 0
    COMPLETE = 1
    KEEP = 2


@dataclasses.dataclass
class Click:

    parser: Any
    cmd: Any = True
    ctx: Any = True

    @functools.singledispatchmethod
    def __call__(self, target: Any) -> Any:
        target.parse_args = self(target.parse_args)
        return target

    @__call__.register
    def _(self, target: types.FunctionType) -> types.FunctionType:
        @functools.wraps(target)
        def ans(cmd, ctx, args):
            p = self.parser.copy()
            if self.cmd:
                p.clickCommand(cmd)
            if self.ctx:
                p.clickContext(ctx)
            return target(cmd, ctx, p.parse_args(args))

        return ans

    @__call__.register
    def _(self, target: types.MethodType) -> types.MethodType:
        func = self(target.__func__)
        ans = types.MethodType(func, target.__self__)
        return ans


class Nargs(enum.IntEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2


@dataclasses.dataclass(kw_only=True)
class PreParser:
    def __init__(
        self,
        optdict: Any = None,
        prog: Any = None,
        abbrev: Any = Abbrev.COMPLETE,
        permutate: Any = True,
        posix: Any = "infer",
    ) -> None:
        self._optdict = dict()
        self.optdict = optdict
        self.prog = prog
        self.abbrev = abbrev
        self.permutate = permutate
        self.posix = posix

    def __repr__(self) -> str:
        "Return repr(self)."
        return datarepr(type(self).__name__, **self.todict())

    @makeprop()
    def abbrev(self, value: SupportsInt) -> Abbrev:
        "Property that decides how to handle abbreviations."
        return Abbrev(value)

    def click(self, cmd: Any = True, ctx: Any = True) -> Click:
        "Return a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    def copy(self) -> Self:
        "Return a copy."
        return type(self)(**self.todict())

    @makeprop()
    def optdict(self, value: Any) -> dict:
        "Dictionary of options."
        if value is None:
            self._optdict.clear()
            return self._optdict
        value = dict(value)
        self._optdict.clear()
        self._optdict.update(value)
        return self._optdict

    def parse_args(
        self,
        args: Optional[Iterable] = None,
    ) -> List[str]:
        "Parse args."
        if args is None:
            args = sys.argv[1:]
        return Parsing(
            parser=self.copy(),
            args=[str(a) for a in args],
        ).ans

    @makeprop()
    def permutate(self, value: Any) -> bool:
        "Property that decides if the arguments will be permutated."
        return bool(value)

    @makeprop()
    def posix(self, value: Any) -> bool:
        "Property that decides if posix parsing is used, "
        "i.e. a positional argument causes all the arguments after it "
        "to be also interpreted as positional."
        if value == "infer":
            value = os.environ.get("POSIXLY_CORRECT")
        value = bool(value)
        return value

    @makeprop()
    def prog(self, value: Any) -> str:
        "Property that represents the name of the program."
        if value is None:
            value = os.path.basename(sys.argv[0])
        return str(value)

    def reflectClickCommand(self, cmd: cl.Command) -> None:
        "Reflect a click.Command object."
        optdict = dict()
        for p in cmd.params:
            if not isinstance(p, cl.Option):
                continue
            if p.is_flag or p.nargs == 0:
                optn = Nargs.NO_ARGUMENT
            elif p.nargs == 1:
                optn = Nargs.REQUIRED_ARGUMENT
            else:
                optn = Nargs.OPTIONAL_ARGUMENT
            for o in p.opts:
                optdict[str(o)] = optn
        self.optdict.clear()
        self.optdict.update(optdict)

    def reflectClickContext(self, ctx: cl.Context) -> None:
        "Reflect a click.Context object."
        self.prog = ctx.info_name

    def todict(self) -> dict:
        "Return a dict representing the current instance."
        return dict(
            optdict=self.optdict,
            prog=self.prog,
            abbrev=self.abbrev,
            permutate=self.permutate,
            posix=self.posix,
        )

    def warn(self, message: Any) -> None:
        "Warn about something."
        warnings.warn("%s: %s" % (self.prog, message))

    def warnAboutUnrecognizedOption(self, option: Any) -> None:
        "Warn about an unrecognized option."
        self.warn("unrecognized option %r" % option)

    def warnAboutInvalidOption(self, option: Any) -> None:
        "Warn about an invalid option."
        self.warn("invalid option -- %r" % option)

    def warnAboutAmbiguousOption(self, option: Any, possibilities: Iterable) -> None:
        "Warn about an ambiguous option."
        msg = "option %r is ambiguous; possibilities:" % option
        for x in possibilities:
            msg += " %r" % x
        self.warn(msg)

    def warnAboutUnallowedArgument(self, option: Any) -> None:
        "Warn about an unallowed argument."
        self.warn("option %r doesn't allow an argument" % option)

    def warnAboutRequiredArgument(self, option: Any) -> None:
        "Warn about a required argument."
        self.warn("option requires an argument -- %r" % option)


@dataclasses.dataclass
class Parsing:
    parser: PreParser
    args: list[str]

    def __post_init__(self) -> None:
        self.ans = list()
        self.spec = list()
        optn = 0
        while self.args:
            optn = self.tick(optn)
        if optn == 1:
            self.lasttick()
        self.dumpspec()

    def dumpspec(self):
        self.ans += self.spec
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
            return True
        return False

    def lasttick(self):
        self.parser.warnAboutRequiredArgument(self.ans[-1])

    @functools.cached_property
    def optdict(self) -> Dict[str, Nargs]:
        ans = dict()
        for k, v in self.parser.optdict.items():
            ans[str(k)] = Nargs(v)
        return ans

    def possibilities(self, opt):
        if opt in self.optdict.keys():
            return [opt]
        if self.parser.abbrev == Abbrev.REJECT:
            return list()
        ans = list()
        for k in self.optdict.keys():
            if k.startswith(opt):
                ans.append(k)
        return ans

    def tick(self, optn):
        arg = self.args.pop(0)
        if optn == "break":
            self.spec.append(arg)
            return "break"
        if optn == 1:
            self.ans.append(arg)
            return 0
        elif arg == "--":
            self.ans.append("--")
            return "break"
        elif arg.startswith("-") and arg != "-":
            return self.tick_opt(arg)
        else:
            return self.tick_pos(arg)

    def tick_opt(self, arg: str):
        if arg.startswith("--") or self.islongonly:
            return self.tick_opt_long(arg)
        else:
            return self.tick_opt_short(arg)

    def tick_opt_long(self, arg: str):
        try:
            i = arg.index("=")
        except ValueError:
            i = len(arg)
        opt = arg[:i]
        possibilities = self.possibilities(opt)
        if len(possibilities) == 0:
            self.parser.warnAboutUnrecognizedOption(arg)
            self.ans.append(arg)
            return 0
        if len(possibilities) > 1:
            self.parser.warnAboutAmbiguousOption(arg, possibilities)
            self.ans.append(arg)
            return 0
        opt = possibilities[0]
        if self.parser.abbrev == Abbrev.COMPLETE:
            self.ans.append(opt + arg[i:])
        else:
            self.ans.append(arg)
        if "=" in arg:
            if self.optdict[opt] == 0:
                self.parser.warnAboutUnallowedArgument(opt)
            return 0
        else:
            return self.optdict[opt]

    def tick_opt_short(self, arg: str):
        self.ans.append(arg)
        nargs = 0
        for i in range(1 - len(arg), 0):
            if nargs != 0:
                return 0
            nargs = self.optdict.get("-" + arg[i])
            if nargs is None:
                self.parser.warnAboutInvalidOption(arg[i])
                nargs = 0
        if nargs == 1:
            return 1
        else:
            return 0

    def tick_pos(self, arg: str):
        self.spec.append(arg)
        if self.parser.posix:
            return "break"
        elif self.parser.permutate:
            return 0
        else:
            self.dumpspec()
            return 0

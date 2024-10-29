import dataclasses
import enum
import functools
import operator
import os
import sys
import types
import warnings
from typing import *

import click as cl
from datarepr import datarepr
from makeprop import makeprop

__all__ = ["Abbrev", "Nargs", "PreParser"]


class Abbrev(enum.IntEnum):
    REJECT = 0
    COMPLETE = 1
    KEEP = 2


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
    ):
        self._optdict = dict()
        self.optdict = optdict
        self.prog = prog
        self.abbrev = abbrev
        self.permutate = permutate
        self.posix = posix

    def __repr__(self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @makeprop()
    def abbrev(self, value):
        return Abbrev(value)

    def click(self, *, cmd=True, ctx=True):
        return Click(parser=self, cmd=cmd, ctx=ctx)

    def clickCommand(self, cmd: cl.Command):
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

    def clickContext(self, ctx: cl.Context):
        self.prog = ctx.info_name

    def copy(self):
        return type(self)(**self.todict())

    @makeprop()
    def optdict(self, value):
        if value is None:
            self._optdict.clear()
            return self._optdict
        value = dict(value)
        self._optdict.clear()
        self._optdict.update(value)
        return self._optdict

    def parse_args(self, args: Optional[Iterable] = None) -> List[str]:
        if args is None:
            args = sys.argv[1:]
        return _Parsing(
            parser=self.copy(),
            args=list(args),
        ).ans

    @makeprop()
    def permutate(self, value):
        return bool(value)

    @makeprop()
    def posix(self, value):
        if value == "infer":
            value = os.environ.get("POSIXLY_CORRECT")
        value = bool(value)
        return value

    @makeprop()
    def prog(self, value):
        if value is None:
            value = os.path.basename(sys.argv[0])
        return str(value)

    def todict(self) -> dict:
        return dict(
            optdict=self.optdict,
            prog=self.prog,
            abbrev=self.abbrev,
            permutate=self.permutate,
            posix=self.posix,
        )

    def warn(self, message):
        warnings.warn("%s: %s" % (self.prog, message))

    def warnAboutUnrecognizedOption(self, option):
        self.warn("unrecognized option %r" % option)

    def warnAboutInvalidOption(self, option):
        self.warn("invalid option -- %r" % option)

    def warnAboutAmbigousOption(self, option, possibilities):
        msg = "option %r is ambiguous; possibilities:" % option
        for x in possibilities:
            msg += " %r" % x
        self.warn(msg)

    def warnAboutNotAllowedArgument(self, option):
        self.warn("option %r doesn't allow an argument" % option)

    def warnAboutRequiredArgument(self, option):
        self.warn("option requires an argument -- %r" % option)


@dataclasses.dataclass
class Click:
    parser: Any
    cmd: Any
    ctx: Any

    def __call__(self, target: Any):
        if isinstance(target, types.FunctionType):
            return self._f(target)
        elif isinstance(target, types.MethodType):
            return self._m(target)
        elif isinstance(target, type):
            return self._t(target)
        else:
            return self._o(target)

    def _f(self, target):
        @functools.wraps(target)
        def ans(cmd, ctx, args):
            p = self.parser.copy()
            if self.cmd:
                p.clickCommand(cmd)
            if self.ctx:
                p.clickContext(ctx)
            return target(cmd, ctx, p.parse_args(args))

        return ans

    def _m(self, target):
        func = self._f(target.__func__)
        ans = types.MethodType(func, target.__self__)
        return ans

    def _t(self, target):
        target.parse_args = self._f(target.parse_args)
        return target

    def _o(self, target):
        target.parse_args = self._m(target.parse_args)
        return target


@dataclasses.dataclass
class _Parsing:
    parser: PreParser
    args: list[str]

    def __post_init__(self):
        self.ans = list()
        self.spec = list()
        optn = 0
        while self.args:
            optn = self.tick(optn)
        if optn == 1:
            self.parser.warnAboutRequiredArgument(self.ans[-1])
        self.ans += self.spec

    @functools.cached_property
    def islongonly(self):
        for k in self.optdict.keys():
            if len(k) < 3:
                continue
            if k.startswith("--"):
                continue
            if not k.startswith("-"):
                continue
            return True
        return False

    @functools.cached_property
    def optdict(self):
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
            if arg.startswith("--") or self.islongonly:
                return self.tick_long(arg)
            else:
                return self.tick_short(arg)
        else:
            if self.parser.posix:
                self.spec.append(arg)
                return "break"
            elif self.parser.permutate:
                self.spec.append(arg)
                return 0
            else:
                self.ans.append(arg)
                return 0

    def tick_long(self, arg: str):
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
            self.parser.warnAboutAmbigousOption(arg, possibilities)
            self.ans.append(arg)
            return 0
        opt = possibilities[0]
        if self.parser.abbrev == Abbrev.COMPLETE:
            self.ans.append(opt + arg[i:])
        else:
            self.ans.append(arg)
        if "=" in arg:
            if self.optdict[opt] == 0:
                self.parser.warnAboutNotAllowedArgument(opt)
            return 0
        else:
            return self.optdict[opt]

    def tick_short(self, arg: str):
        self.ans.append(arg)
        for i in range(1 - len(arg), 0):
            optn = self.optdict.get("-" + arg[i])
            if optn is None:
                self.parser.warnAboutInvalidOption(arg[i])
                optn = 0
            if i != -1 and optn != 0:
                return 0
            if i == -1 and optn == 1:
                return 1
        return 0

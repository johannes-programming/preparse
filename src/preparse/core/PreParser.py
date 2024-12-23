import dataclasses
import os
import sys
import warnings
from typing import *

import click as cl
from datarepr import datarepr
from makeprop import makeprop

from preparse._parsing.Parsing import *
from preparse.core.Click import *
from preparse.core.enums import *

__all__ = ["PreParser"]


@dataclasses.dataclass(kw_only=True)
class PreParser:
    def __init__(
        self,
        optdict: Any = None,
        prog: Any = None,
        longOptionAbbreviations: Any = LongOptionAbbreviations.COMPLETE,
        permutate: Any = True,
        posix: Any = "infer",
    ) -> None:
        self._optdict = dict()
        self.optdict = optdict
        self.prog = prog
        self.longOptionAbbreviations = longOptionAbbreviations
        self.permutate = permutate
        self.posix = posix

    def __repr__(self) -> str:
        "This magic methods gives repr(self)."
        return datarepr(type(self).__name__, **self.todict())

    @makeprop()
    def longOptionAbbreviations(self, value: SupportsInt) -> LongOptionAbbreviations:
        "This property decides how to handle abbreviations."
        return LongOptionAbbreviations(value)

    def click(self, cmd: Any = True, ctx: Any = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    def copy(self) -> Self:
        "This method returns a copy of the current instance."
        return type(self)(**self.todict())

    @makeprop()
    def optdict(self, value: Any) -> dict:
        "This property gives a dictionary of options."
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
    ) -> list[str]:
        "This method parses args."
        if args is None:
            args = sys.argv[1:]
        return Parsing(
            parser=self.copy(),
            args=[str(a) for a in args],
        ).ans

    @makeprop()
    def permutate(self, value: Any) -> bool:
        "This property decides if the arguments will be permutated."
        return bool(value)

    @makeprop()
    def posix(self, value: Any) -> bool:
        "This property decides if posix parsing is used,"
        "i.e. a positional argument causes all the arguments after it "
        "to be also interpreted as positional."
        if value == "infer":
            value = os.environ.get("POSIXLY_CORRECT")
        value = bool(value)
        return value

    @makeprop()
    def prog(self, value: Any) -> str:
        "This property represents the name of the program."
        if value is None:
            value = os.path.basename(sys.argv[0])
        return str(value)

    def reflectClickCommand(self, cmd: cl.Command) -> None:
        "This method causes the current instance to reflect a click.Command object."
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
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name

    def todict(self) -> dict:
        "This method returns a dict representing the current instance."
        return dict(
            optdict=self.optdict,
            prog=self.prog,
            longOptionAbbreviations=self.longOptionAbbreviations,
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

from __future__ import annotations

import os
import sys
import types
from typing import *

import click as cl
import namings
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import *
from preparse._utils.dataprop import dataprop
from preparse.core.Click import Click
from preparse.core.enums import *
from preparse.core.OptNaming import OptNaming
from preparse.core.warnings import *

__all__ = ["PreParser"]


class PreParser(Copyable):

    abbr: Optional[Tuning]
    allowslong: bool
    allowsshort: bool
    bundling: Tuning
    expectsPOSIX: bool
    optNaming: OptNaming
    prog: str
    reconcilesorders: bool
    special: Tuning
    warn: types.FunctionType

    __slots__ = ("_data",)

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        abbr: Optional[Tuning] = Tuning.MINIMIZE,
        allowslong: Any = True,
        allowsshort: Any = True,
        bundling: Any = Tuning.MAINTAIN,
        expectsPOSIX: Any = False,
        optNaming: Any = (),
        prog: Any = None,
        reconcilesorders: Any = True,
        special: Any = Tuning.MAINTAIN,
        warn: Callable = str,
    ) -> None:
        self.abbr = abbr
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.bundling = bundling
        self.expectsPOSIX = expectsPOSIX
        self.optNaming = optNaming
        self.prog = prog
        self.reconcilesorders = reconcilesorders
        self.special = special
        self.warn = warn

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.toNaming())

    @dataprop
    def abbr(self: Self, value: Any) -> bool:
        if value is not None:
            return Tuning(value)

    @dataprop
    def allowslong(self: Self, value: Any) -> bool:
        return bool(value)

    @dataprop
    def allowsshort(self: Self, value: Any) -> bool:
        return bool(value)

    @dataprop
    def bundling(self: Self, value: Any) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return Tuning(value)

    def click(self: Self, cmd: Any = True, ctx: Any = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.toNaming())

    @dataprop
    def expectsPOSIX(self: Self, value: Any) -> bool:
        if value == "infer":
            return bool(os.environ.get("POSIXLY_CORRECT"))
        else:
            return bool(value)

    @dataprop
    def optNaming(self: Self, value: Any) -> OptNaming:
        "This property gives a naming of options."
        if "optNaming" not in self._data.keys():
            self._data["optNaming"] = OptNaming()
        self._data["optNaming"].data = value
        return self._data["optNaming"]

    def parse_args(
        self: Self,
        args: Optional[Iterable] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.toNaming())

    @dataprop
    def prog(self: Self, value: Any) -> str:
        "This property represents the name of the program."
        if value is None:
            return str(os.path.basename(sys.argv[0]))
        else:
            return str(value)

    @dataprop
    def reconcilesorders(self: Self, value: Any) -> bool:
        return bool(value)

    def reflectClickCommand(self: Self, cmd: cl.Command) -> None:
        "This method causes the current instance to reflect a click.Command object."
        nargs: Nargs
        opt: Any
        optNaming: namings.Naming[Nargs]
        param: Any
        optNaming = namings.Naming()
        for param in cmd.params:
            if not isinstance(param, cl.Option):
                continue
            if param.is_flag or param.nargs == 0:
                nargs = Nargs.NO_ARGUMENT
            elif param.nargs == 1:
                nargs = Nargs.REQUIRED_ARGUMENT
            else:
                nargs = Nargs.OPTIONAL_ARGUMENT
            for opt in param.opts:
                optNaming[opt] = nargs
        self.optNaming.clear()
        self.optNaming.update(optNaming)

    def reflectClickContext(self: Self, ctx: cl.Context) -> None:
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name

    @dataprop
    def special(self: Self, value: Any) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return Tuning(value)

    def toNaming(self: Self) -> namings.Naming:
        "This method returns a naming representing the current instance."
        ans: namings.Naming
        try:
            ans = self._data
        except AttributeError:
            self._data = namings.Naming()
            return namings.Naming()
        else:
            return namings.Naming(ans)

    @dataprop
    def warn(self: Self, value: Callable) -> types.FunctionType:
        "This property gives a function that takes in the warnings."
        return tofunc(value)

from __future__ import annotations

import os
import sys
import types
from typing import *

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import *
from preparse._utils.dataprop import dataprop
from preparse.core.Click import Click
from preparse.core.OptDict import OptDict
from preparse.enums import *
from preparse.warners import *

__all__ = ["PreParser"]


class PreParser(Copyable):

    allowslong: bool
    allowsshort: bool
    bundling: Tuning
    expandsabbr: bool
    expectsabbr: bool
    expectsposix: bool
    optDict: OptDict
    prog: str
    reconcilesorders: bool
    special: Tuning
    warn: Callable

    __slots__ = ("_data",)

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        allowslong: Any = True,
        allowsshort: Any = True,
        bundling: Any = Tuning.MAINTAIN,
        expandsabbr: Any = True,
        expectsabbr: Any = True,
        expectsposix: Any = False,
        optDict: Any = (),
        prog: Any = None,
        reconcilesorders: Any = True,
        special: Any = Tuning.MAINTAIN,
        warn: types.FunctionType = str,
    ) -> None:
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix
        self.optDict = optDict
        self.prog = prog
        self.reconcilesorders = reconcilesorders
        self.special = special
        self.warn = warn

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

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
        return type(self)(**self.todict())

    @dataprop
    def expandsabbr(self: Self, value: Any) -> bool:
        return bool(value)

    @dataprop
    def expectsabbr(self: Self, value: Any) -> bool:
        return bool(value)

    @dataprop
    def expectsposix(self: Self, value: Any) -> bool:
        if value == "infer":
            return bool(os.environ.get("POSIXLY_CORRECT"))
        else:
            return bool(value)

    @dataprop
    def optDict(self: Self, value: Any) -> OptDict:
        "This property gives a dictionary of options."
        dataA: OptDict
        if "optDict" not in self._data.keys():
            self._data["optDict"] = OptDict()
        dataA = OptDict(value)
        self._data["optDict"].clear()
        self._data["optDict"].update(dataA)
        return self._data["optDict"]

    def parse_args(
        self: Self,
        args: Optional[Iterable] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

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
        optDict: dict[str, Nargs]
        nargs: Nargs
        opt: Any
        param: Any
        optDict = dict()
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
                optDict[str(opt)] = nargs
        self.optDict.clear()
        self.optDict.update(optDict)

    def reflectClickContext(self: Self, ctx: cl.Context) -> None:
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name

    @dataprop
    def special(self: Self, value: Any) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return Tuning(value)

    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans: dict
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            return dict()
        else:
            return dict(ans)

    @dataprop
    def warn(self: Self, value: Callable) -> types.FunctionType:
        "This property gives a function that takes in the warnings."
        return tofunc(value)

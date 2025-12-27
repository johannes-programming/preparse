import os
import sys
import types
from typing import *

import click as cl
import setdoc
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import *
from preparse.core.Click import *
from preparse.core.enums import *
from preparse.core.Optdict import *
from preparse.core.warnings import *

__all__ = ["PreParser"]


class PreParser:

    __slots__ = ("_data",)

    allowslong: bool
    allowsshort: bool
    bundling: Tuning
    expandsabbr: bool
    expectsabbr: bool
    expectsposix: bool
    optdict: Optdict
    prog: str
    reconcilesorders: bool
    special: Tuning
    warn: types.FunctionType

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
        optdict: Any = (),
        prog: Any = None,
        reconcilesorders: Any = True,
        special: Any = Tuning.MAINTAIN,
        warn: Callable = str,
    ) -> None:
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix
        self.optdict = optdict
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
    def optdict(self: Self, value: Any) -> Optdict:
        "This property gives a dictionary of options."
        dataA: Optdict
        if "optdict" not in self._data.keys():
            self._data["optdict"] = Optdict()
        dataA = Optdict(value)
        self._data["optdict"].clear()
        self._data["optdict"].update(dataA)
        return self._data["optdict"]

    def parse_args(
        self: Self,
        args: Optional[Iterable] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    @dataprop
    def prog(self: Self, value: Any) -> str:
        "This property represents the name of the program."
        v: Any
        if value is None:
            v = os.path.basename(sys.argv[0])
        else:
            v = value
        return str(v)

    @dataprop
    def reconcilesorders(self: Self, value: Any) -> bool:
        return bool(value)

    def reflectClickCommand(self: Self, cmd: cl.Command) -> None:
        "This method causes the current instance to reflect a click.Command object."
        optdict: dict[str, Nargs]
        nargs: Nargs
        opt: Any
        param: Any
        optdict = dict()
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
                optdict[str(opt)] = nargs
        self.optdict.clear()
        self.optdict.update(optdict)

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
            ans = dict()
        else:
            ans = dict(ans)
        return ans

    @dataprop
    def warn(self: Self, value: Callable) -> types.FunctionType:
        "This property gives a function that takes in the warnings."
        return tofunc(value)

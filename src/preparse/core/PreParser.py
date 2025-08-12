import os
import sys
import types
from typing import *

import click as cl
from datarepr import datarepr
from makeprop import makeprop
from tofunc import tofunc

from preparse._processing import *
from preparse.core.Click import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["PreParser"]


class BasePreParser:
    __slots__ = (
        "_allowslong",
        "_bundling",
        "_expandsabbr",
        "_expectsabbr",
        "_expectsposix",
        "_optdict",
        "_prog",
        "_reconcilesorders",
        "_warn",
    )

    def __init__(
        self: Self, *,
        optdict: Any = None,
        prog: Any = None,
        expectsabbr:Any = True,
        expandsabbr:Any = True,
        bundling: Any = Tuning.MAINTAIN,
        allowslong: Any = False,
        expectsposix:Any=False,
        reconcilesorders:Any=True,
        warn: Callable = str,
    ) -> None:
        "This magic method initializes self."
        self.optdict = optdict
        self.prog = prog
        self.expectsabbr = expectsabbr
        self.expandsabbr = expandsabbr
        self.bundling = bundling
        self.allowslong = allowslong
        self.expectsposix = expectsposix
        self.reconcilesorders = reconcilesorders
        self.warn = warn
    def __repr__(self: Self) -> str:
        "This magic method implements repr(self)."
        return datarepr(type(self).__name__, **self.todict())

    def copy(self: Self) -> Self:
        "This method returns a copy of the current instance."
        return type(self)(**self.todict())
    
    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans = dict()
        for slot in type(self).__slots__:
            name = slot.lstrip("_")
            ans[name] = getattr(self, slot)
        return ans

    @makeprop()
    def expectsabbr(self: Self, value: Any) -> bool:
        return bool(value)
    @makeprop()
    def expandsabbr(self: Self, value: Any) -> bool:
        return bool(value)
    @makeprop()
    def bundling(self: Self, value: Any) -> dict:
        "This property decides how to approach the bundling of short options."
        return Tuning(value)
    @makeprop()
    def allowslong(self: Self, value: Any) -> bool:
        "This property decides whether the parser treats all options as long."
        return bool(value)
    @makeprop()
    def optdict(self: Self, value: Any) -> dict:
        "This property gives a dictionary of options."
        dataA:dict 
        if value is None:
            dataA = dict()
        else:
            dataA = dict(value)
        dataB:dict=dict()
        k:str
        v:Nargs
        for k, v in dataA.items():
            dataB[str(k)] = Nargs(v)
        self._optdict = dict(dataB)
        return dataB

    @makeprop()
    def expectsposix(self: Self, value: Any) -> bool:
        return bool(value)
    @makeprop()
    def reconcilesorders(self: Self, value: Any) -> bool:
        return bool(value)

    @makeprop()
    def prog(self: Self, value: Any) -> str:
        "This property represents the name of the program."
        if value is None:
            value = os.path.basename(sys.argv[0])
        return str(value)
    
    @makeprop()
    def warn(self: Self, value: Callable) -> types.FunctionType:
        "This property gives a function that takes in the warnings."
        return tofunc(value)


class PreParser(BasePreParser):

    
    def cause_warning(self: Self, wrncls:type, /, **kwargs:Any) -> None:
        warning:PreparseWarning=wrncls(prog=self.prog, **kwargs)
        self.warn(warning)

    def click(self: Self, cmd: Any = True, ctx: Any = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)


    def parse_args(
        self: Self,
        args: Optional[Iterable] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args=args, parser=self)
    


    def reflectClickCommand(self: Self, cmd: cl.Command) -> None:
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

    def reflectClickContext(self: Self, ctx: cl.Context) -> None:
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name



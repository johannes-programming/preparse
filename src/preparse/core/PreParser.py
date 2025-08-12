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
        "_abbr",
        "_bundling",
        "_longonly",
        "_optdict",
        "_order",
        "_prog",
        "_warn",
    )

    def __init__(
        self: Self, *,
        optdict: Any = None,
        prog: Any = None,
        abbr: Any = Abbr.COMPLETE,
        bundling: Any = Tuning.MAINTAIN,
        longonly: Any = False,
        order: Any = Order.PERMUTE,
        warn: Callable = str,
    ) -> None:
        "This magic method initializes self."
        self.optdict = optdict
        self.prog = prog
        self.abbr = abbr
        self.bundling = bundling
        self.longonly = longonly
        self.order = order
        self.warn = warn

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
    def abbr(self: Self, value: SupportsInt) -> Abbr:
        "This property decides how to handle abbreviations."
        return Abbr(value)
    @makeprop()
    def bundling(self: Self, value: Any) -> dict:
        "This property decides how to approach the bundling of short options."
        return Tuning(value)
    @makeprop()
    def longonly(self: Self, value: Any) -> bool:
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
    def order(self: Self, value: Any) -> Order:
        "This property decides how to order flags and positional arguments."
        if value == "infer_given":
            return Order.infer_given()
        if value == "infer_permute":
            return Order.infer_permute()
        return Order(value)

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

    def __repr__(self: Self) -> str:
        "This magic method implements repr(self)."
        return datarepr(type(self).__name__, **self.todict())

    
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



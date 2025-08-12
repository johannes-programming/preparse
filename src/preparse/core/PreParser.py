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
        # options
        "_allowslong",
        "_allowsshort",
        "_optdict",

        # warnings
        "_prog",
        "_warn",

        # orders
        "_expectsposix",
        "_reconcilesorders",

        # abbr
        "_expectsabbr",
        "_expandsabbr",

        # tuning
        "_bundling",
        "_special",
    )

    def __init__(
        self: Self, *,

        # options
        allowslong:Any = True,
        allowsshort:Any = True,
        optdict:Any= None,

        # warnings
        prog:Any = None,
        warn:Callable=str,

        # orders
        expectsposix:Any = False,
        reconcilesorders:Any = True,

        # abbr
        expectsabbr:Any = True,
        expandsabbr:Any = True,

        # tuning
        bundling:Tuning = Tuning.MAINTAIN,
        special:Tuning = Tuning.MAXIMIZE,
    ) -> None:
        "This magic method initializes self."
        # options
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.optdict = optdict

        # warnings
        self.prog = prog 
        self.warn = warn

        # orders
        self.expectsposix = expectsposix
        self.reconcilesorders = reconcilesorders

        # abbr
        self.expectsabbr = expectsabbr
        self.expandsabbr = expandsabbr

        # tuning
        self.bundling = bundling
        self.special = special

    # options
    @makeprop()
    def allowslong(self:Self, value:Any)->bool:
        return bool(value)

    @makeprop()
    def allowsshort(self:Self, value:Any)->bool:
        return bool(value)

    @property
    def optdict(self:Self)->dict:
        return dict(self._optdict)
    @optdict.setter
    def optdict(self:Self, value:Any)->None:
        if value is None:
            self._optdict = dict()
            return
        dataA:dict = dict(value)
        dataB:dict = dict()
        k:Any
        v:Any
        for k, v in dataA.items():
            dataB[str(k)] = Nargs(v)
        self._optdict = dataB
    
    # warnings
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
    
    # orders
    @makeprop()
    def expectsposix(self:Self, value: Any) -> bool:
        if value == "infer":
            value = os.environ.get("POSIXLY_CORRECT")
        return bool(value)
    
    @makeprop()
    def reconcilesorders(self:Self, value: Any) -> bool:
        return bool(value)
    
    # abbr
    @makeprop()
    def expectsabbr(self:Self, value:Any)->bool:
        return bool(value)
    @makeprop()
    def expandsabbr(self:Self, value:Any)->bool:
        return bool(value)
    
    # tuning
    @makeprop()
    def bundling(self:Self, value:Any)->Tuning:
        return Tuning(value)
    @makeprop()
    def special(self:Self, value:Any)->Tuning:
        return Tuning(value)






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

    def copy(self: Self) -> Self:
        "This method returns a copy of the current instance."
        return type(self)(**self.todict())

    def parse_args(
        self: Self,
        args: Optional[Iterable] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    
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

    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans = dict()
        for slot in type(self).__slots__:
            name = slot.lstrip("_")
            ans[name] = getattr(self, slot)
        return ans
    
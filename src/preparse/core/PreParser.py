from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
import sys
from collections.abc import Callable, Hashable, Iterable
from typing import Any, Self, cast

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._core.Framework import Framework
from preparse._core.no_change_setter import no_change_setter
from preparse._core.Transformation import Transformation
from preparse._processing import process
from preparse.core.Click import Click
from preparse.core.Optdict import Optdict
from preparse.enums.Nargs import Nargs
from preparse.enums.NoChange import NoChange
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from preparse.warnings.PreparseWarning import PreparseWarning


class PreParser(Copyable):
    _framework: Framework
    _optdict: Optdict
    _transformation: Transformation

    __slots__ = ("_framework", "_optdict", "_transformation")

    @setdoc.basic
    def __init__(
        self: Self,
        other: PreParser | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        allowslong: SupportsBool | NoChange = NoChange.NO_CHANGE,
        allowsshort: SupportsBool | NoChange = NoChange.NO_CHANGE,
        bundling: int | NoChange = NoChange.NO_CHANGE,
        expandsabbr: SupportsBool | NoChange = NoChange.NO_CHANGE,
        expectsabbr: SupportsBool | NoChange = NoChange.NO_CHANGE,
        expectsposix: SupportsBool | NoChange = NoChange.NO_CHANGE,
        optdict: (
            SupportsKeysAndGetitem
            | Iterable[tuple[Hashable, object]]
            | NoChange
        ) = NoChange.NO_CHANGE,
        prog: object | NoChange = NoChange.NO_CHANGE,
        reconcilesorders: SupportsBool | NoChange = NoChange.NO_CHANGE,
        special: int | NoChange = NoChange.NO_CHANGE,
        warn: Callable[[PreparseWarning], Any] | NoChange = NoChange.NO_CHANGE,
    ) -> None:
        self._framework = Framework()
        self._optdict = Optdict()
        self._transformation = Transformation()
        self._init_other(other)
        self._framework.allowslong = allowslong
        self._framework.allowsshort = allowsshort
        self._framework.expectsabbr = expectsabbr
        self._framework.expectsposix = expectsposix
        self.optdict.data = optdict
        self._transformation.bundling = bundling
        self._transformation.expandsabbr = expandsabbr
        self._transformation.prog = prog
        self._transformation.reconcilesorders = reconcilesorders
        self._transformation.special = special
        self._transformation.warn = warn

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @no_change_setter
    def _init_other(self: Self, other: PreParser, /) -> None:
        self._framework._init_other(other._framework)
        self.optdict.data = other.optdict
        self._transformation._init_other(other._transformation)

    @property
    def allowslong(self: Self, /) -> bool:
        return self._framework.allowslong

    @allowslong.setter
    @no_change_setter
    def allowslong(self: Self, value: SupportsBool, /) -> None:
        self._framework.allowslong = value

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._framework.allowsshort

    @allowsshort.setter
    @no_change_setter
    def allowsshort(self: Self, value: SupportsBool, /) -> None:
        self._framework.allowsshort = value

    @property
    def bundling(self: Self, /) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._transformation.bundling

    @bundling.setter
    @no_change_setter
    def bundling(self: Self, value: int, /) -> None:
        "This property decides how to approach the bundling of short options."
        self._transformation.bundling = Tuning(value)

    def click(
        self: Self, /, cmd: SupportsBool = True, ctx: SupportsBool = True
    ) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(**self.todict())

    @property
    def expandsabbr(self: Self, /) -> bool:
        return self._transformation.expandsabbr

    @expandsabbr.setter
    @no_change_setter
    def expandsabbr(self: Self, value: SupportsBool, /) -> None:
        self._transformation.expandsabbr = value

    @property
    def expectsabbr(self: Self, /) -> bool:
        return self._framework.expectsabbr

    @expectsabbr.setter
    @no_change_setter
    def expectsabbr(self: Self, value: SupportsBool, /) -> None:
        self._framework.expectsabbr = value

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._framework.expectsposix

    @expectsposix.setter
    @no_change_setter
    def expectsposix(self: Self, value: SupportsBool, /) -> None:
        self._framework.expectsposix = value

    @property
    def optdict(self: Self, /) -> Optdict:
        "This property gives a dictionary of options."
        return self._optdict

    @optdict.setter
    @no_change_setter
    def optdict(self: Self, value: Any, /) -> None:
        "This property gives a dictionary of options."
        self._optdict.data = value

    def parse_args(
        self: Self,
        /,
        args: Iterable[object] | None = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    @property
    def prog(self: Self, /) -> str:
        "This property represents the name of the program."
        return self._transformation.prog

    @prog.setter
    @no_change_setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        self._transformation.prog = value

    @property
    def reconcilesorders(self: Self, /) -> bool:
        return self._transformation.reconcilesorders

    @reconcilesorders.setter
    @no_change_setter
    def reconcilesorders(self: Self, value: SupportsBool, /) -> None:
        self._transformation.reconcilesorders = value

    def reflectClickCommand(self: Self, /, cmd: cl.Command) -> None:
        "This method causes the current instance to reflect a click.Command object."
        nargs: Nargs
        opt: Any
        optdict: dict[str, Nargs]
        param: Any
        optdict = dict()
        for param in cmd.params:
            if not isinstance(param, cl.Option):
                continue
            if param.is_flag:
                nargs = Nargs.NO_ARGUMENT
            elif not param.nargs:
                nargs = Nargs.NO_ARGUMENT
            elif param.flag_value is not None:
                nargs = Nargs.OPTIONAL_ARGUMENT
            elif param.prompt and not param.prompt_required:
                nargs = Nargs.OPTIONAL_ARGUMENT
            else:
                nargs = Nargs.REQUIRED_ARGUMENT
            for opt in param.opts + param.secondary_opts:
                optdict[opt] = nargs
        self.optdict.clear()
        self.optdict.update(optdict)

    def reflectClickContext(self: Self, /, ctx: cl.Context) -> None:
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name

    @property
    def special(self: Self, /) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return self._transformation.special

    @special.setter
    @no_change_setter
    def special(self: Self, value: int, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        self._transformation.special = value

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        ans = self._framework.todict()
        ans |= dict(optdict=self.optdict)
        ans |= self._transformation.todict()
        return dict(sorted(ans.items()))

    @property
    def warn(
        self: Self,
        /,
    ) -> Callable[[PreparseWarning], Any]:
        "This property gives a function that takes in the warnings."
        return self._transformation.warn

    @warn.setter
    @no_change_setter
    def warn(
        self: Self,
        value: Callable[[PreparseWarning], Any],
        /,
    ) -> None:
        "This property gives a function that takes in the warnings."
        self._transformation.warn = tofunc(value)

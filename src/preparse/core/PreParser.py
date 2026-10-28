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

from preparse._core.FrameworkSettings import FrameworkSettings
from preparse._core.TransformationSettings import TransformationSettings
from preparse._processing import process
from preparse.core.Click import Click
from preparse.core.Optdict import Optdict
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from preparse.warnings.PreparseWarning import PreparseWarning


class PreParser(Copyable):
    _frameworkSettings: FrameworkSettings
    _optdict: Optdict
    _transformationSettings: TransformationSettings

    __slots__ = ("_frameworkSettings", "_optdict", "_transformationSettings")

    @setdoc.basic
    def __init__(
        self: Self,
        other: PreParser | None = None,
        /,
        *,
        frameworkSettings: FrameworkSettings|None = None,
        optdict: Optdict | None = None,
        transformationSettings: TransformationSettings|None =None,
    ) -> None:
        self._frameworkSettings = FrameworkSettings()
        self._optdict = Optdict()
        self._transformationSettings = TransformationSettings()
        if other is not None:
            self.frameworkSettings = other.frameworkSettings
            self.optdict = other.optdict
            self.transformationSettings = other.transformationSettings
        self.frameworkSettings = frameworkSettings
        self.optdict = optdict
        self.transformationSettings = transformationSettings
        
    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def frameworkSettings(self: Self, /) -> bool:
        return self._frameworkSettings

    @frameworkSettings.setter
    def frameworkSettings(self: Self, value: SupportsBool, /) -> None:
        self.frameworkSettings.__init__(value)

    def click(
        self: Self, /, cmd: SupportsBool = True, ctx: SupportsBool = True
    ) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def optdict(self: Self, /) -> Optdict:
        "This property gives a dictionary of options."
        return self._optdict

    @optdict.setter
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
        return self._transformationSettings.prog

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        self._transformationSettings.prog = value

    @property
    def reconcilesorders(self: Self, /) -> bool:
        return self._transformationSettings.reconcilesorders

    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: SupportsBool, /) -> None:
        self._transformationSettings.reconcilesorders = value

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
        return self._transformationSettings.special

    @special.setter
    def special(self: Self, value: int, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        self._transformationSettings.special = value

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        ans = self._frameworkSettings.todict()
        ans |= dict(optdict=self.optdict)
        ans |= self._transformationSettings.todict()
        return dict(sorted(ans.items()))

    @property
    def warn(
        self: Self,
        /,
    ) -> Callable[[PreparseWarning], Any]:
        "This property gives a function that takes in the warnings."
        return self._transformationSettings.warn

    @warn.setter
    def warn(
        self: Self,
        value: Callable[[PreparseWarning], Any],
        /,
    ) -> None:
        "This property gives a function that takes in the warnings."
        self._transformationSettings.warn = tofunc(value)

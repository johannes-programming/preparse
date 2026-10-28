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
        /,
        *,
        allowslong: object = True,
        allowsshort: object = True,
        bundling: int = Tuning.MAINTAIN,
        expandsabbr: object = True,
        expectsabbr: object = True,
        expectsposix: object = False,
        optdict: (
            SupportsKeysAndGetitem | Iterable[tuple[Hashable, object]]
        ) = (),
        prog: object = None,
        reconcilesorders: object = True,
        special: int = Tuning.MAINTAIN,
        warn: Callable[[PreparseWarning], Any] = str,
    ) -> None:
        self._frameworkSettings = FrameworkSettings(
            allowslong=allowslong,
            allowsshort=allowsshort,
            expectsabbr=expectsabbr,
            expectsposix=expectsposix,
        )
        self._optdict = Optdict(optdict)
        self._transformationSettings = TransformationSettings(
            bundling=bundling,
            expandsabbr=expandsabbr,
            prog=prog,
            reconcilesorders=reconcilesorders,
            special=special,
            warn=warn,
        )

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self) -> bool:
        return self._frameworkSettings.allowslong

    @allowslong.setter
    def allowslong(self: Self, value: object) -> None:
        self._frameworkSettings.allowslong = value

    @property
    def allowsshort(self: Self) -> bool:
        return self._frameworkSettings.allowsshort

    @allowsshort.setter
    def allowsshort(self: Self, value: object) -> None:
        self._frameworkSettings.allowsshort = value

    @property
    def bundling(self: Self) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._transformationSettings.bundling

    @bundling.setter
    def bundling(self: Self, value: int) -> None:
        "This property decides how to approach the bundling of short options."
        self._transformationSettings.bundling = Tuning(value)

    def click(self: Self, cmd: object = True, ctx: object = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @property
    def expandsabbr(self: Self) -> bool:
        return self._transformationSettings.expandsabbr

    @expandsabbr.setter
    def expandsabbr(self: Self, value: object, /) -> None:
        self._transformationSettings.expandsabbr = value

    @property
    def expectsabbr(self: Self) -> bool:
        return self._frameworkSettings.expectsabbr

    @expectsabbr.setter
    def expectsabbr(self: Self, value: object) -> None:
        self._frameworkSettings.expectsabbr = value

    @property
    def expectsposix(self: Self) -> bool:
        return self._frameworkSettings.expectsposix

    @expectsposix.setter
    def expectsposix(self: Self, value: object) -> None:
        value_: Any
        if value == "infer":
            value_ = os.environ.get("POSIXLY_CORRECT")
        else:
            value_ = value
        self._frameworkSettings.expectsposix = value_

    @property
    def optdict(self: Self) -> Optdict:
        "This property gives a dictionary of options."
        return self._optdict

    @optdict.setter
    def optdict(self: Self, value: Any) -> None:
        "This property gives a dictionary of options."
        value_: Optdict
        value_ = Optdict(value)
        self._optdict.clear()
        self._optdict.update(value_)

    def parse_args(
        self: Self,
        args: Iterable[object] | None = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    @property
    def prog(self: Self) -> str:
        "This property represents the name of the program."
        return self._transformationSettings.prog

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        if value is None:
            self._transformationSettings.prog = os.path.basename(sys.argv[0])
        else:
            self._transformationSettings.prog = value

    @property
    def reconcilesorders(self: Self) -> bool:
        return self._transformationSettings.reconcilesorders

    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: object, /) -> None:
        self._transformationSettings.reconcilesorders = value

    def reflectClickCommand(self: Self, cmd: cl.Command) -> None:
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

    def reflectClickContext(self: Self, ctx: cl.Context) -> None:
        "This method causes the current instance to reflect a click.Context object."
        self.prog = ctx.info_name

    @property
    def special(self: Self) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return self._transformationSettings.special

    @special.setter
    def special(self: Self, value: int, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        self._transformationSettings.special = value

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        ans = self._frameworkSettings.todict()
        ans |= dict(optdict=self.optdict)
        ans |= self._transformationSettings.todict()
        return dict(tuple(ans.items()))

    @property
    def warn(
        self: Self,
    ) -> Callable[[PreparseWarning], Any]:
        "This property gives a function that takes in the warnings."
        return self._transformationSettings.warn

    @warn.setter
    def warn(
        self: Self,
        value: Callable[[PreparseWarning], Any],
    ) -> None:
        "This property gives a function that takes in the warnings."
        self._transformationSettings.warn = tofunc(value)

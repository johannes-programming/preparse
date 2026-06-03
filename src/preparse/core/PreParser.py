from __future__ import annotations

import os
import sys
from collections.abc import Callable, Iterable
from typing import Any, Optional, Self, cast

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import process
from preparse.core.Click import Click
from preparse.core.Optdict import Optdict
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.warnings.PreparseWarning import PreparseWarning

__all__ = ["PreParser"]


class PreParser(Copyable):

    __slots__ = ("_data",)

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        allowslong: object = True,
        allowsshort: object = True,
        bundling: int = Tuning.MAINTAIN,
        expandsabbr: object = True,
        expectsabbr: object = True,
        expectsposix: object = False,
        optdict: Any = (),
        prog: object = None,
        reconcilesorders: object = True,
        special: int = Tuning.MAINTAIN,
        warn: Callable[[PreparseWarning], Any] = str,  # type: ignore[type-arg]
    ) -> None:
        self._data: dict[str, Any]
        self._data = dict()
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

    @property
    def allowslong(self: Self) -> bool:
        return cast(bool, self._data["allowslong"])

    @allowslong.setter
    def allowslong(self: Self, value: object) -> None:
        self._data["allowslong"] = bool(value)

    @property
    def allowsshort(self: Self) -> bool:
        return cast(bool, self._data["allowsshort"])

    @allowsshort.setter
    def allowsshort(self: Self, value: object) -> None:
        self._data["allowsshort"] = bool(value)

    @property
    def bundling(self: Self) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return cast(Tuning, self._data["bundling"])

    @bundling.setter
    def bundling(self: Self, value: int) -> None:
        "This property decides how to approach the bundling of short options."
        self._data["bundling"] = Tuning(value)

    def click(self: Self, cmd: object = True, ctx: object = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @property
    def expandsabbr(self: Self) -> bool:
        return cast(bool, self._data["expandsabbr"])

    @expandsabbr.setter
    def expandsabbr(self: Self, value: object, /) -> None:
        self._data["expandsabbr"] = bool(value)

    @property
    def expectsabbr(self: Self) -> bool:
        return cast(bool, self._data["expectsabbr"])

    @expectsabbr.setter
    def expectsabbr(self: Self, value: object) -> None:
        self._data["expectsabbr"] = bool(value)

    @property
    def expectsposix(self: Self) -> bool:
        return cast(bool, self._data["expectsposix"])

    @expectsposix.setter
    def expectsposix(self: Self, value: object) -> None:
        value_: Any
        if value == "infer":
            value_ = os.environ.get("POSIXLY_CORRECT")
        else:
            value_ = value
        self._data["expectsposix"] = bool(value_)

    @property
    def optdict(self: Self) -> Optdict:
        "This property gives a dictionary of options."
        return cast(Optdict, self._data["optdict"])

    @optdict.setter
    def optdict(self: Self, value: Any) -> None:
        "This property gives a dictionary of options."
        value_: Optdict
        if "optdict" not in self._data.keys():
            self._data["optdict"] = Optdict()
        value_ = Optdict(value)
        self._data["optdict"].clear()
        self._data["optdict"].update(value_)

    def parse_args(
        self: Self,
        args: Optional[Iterable[object]] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    @property
    def prog(self: Self) -> str:
        "This property represents the name of the program."
        return cast(str, self._data["prog"])

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        if value is None:
            self._data["prog"] = str(os.path.basename(sys.argv[0]))
        else:
            self._data["prog"] = str(value)

    @property
    def reconcilesorders(self: Self) -> bool:
        return cast(bool, self._data["reconcilesorders"])

    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: object, /) -> None:
        self._data["reconcilesorders"] = bool(value)

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

    @property
    def special(self: Self) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return cast(Tuning, self._data["special"])

    @special.setter
    def special(self: Self, value: int, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        self._data["special"] = Tuning(value)

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            return dict()
        else:
            return dict(ans)

    @property
    def warn(
        self: Self,
    ) -> Callable[[PreparseWarning], Any]:
        "This property gives a function that takes in the warnings."
        return cast(Callable[[PreparseWarning], Any], self._data["warn"])

    @warn.setter
    def warn(
        self: Self,
        value: Callable[[PreparseWarning], Any],
    ) -> None:
        "This property gives a function that takes in the warnings."
        self._data["warn"] = tofunc(value)

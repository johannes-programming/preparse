from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
import sys
import types
from collections.abc import Callable, Iterable
from typing import Any, Self

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import process
from preparse.core.Click import Click
from preparse.core.enums import Nargs, Tuning
from preparse.core.Optdict import Optdict


class PreParser(Copyable):

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
        optdict: Any = (),
        prog: Any = None,
        reconcilesorders: Any = True,
        special: Any = Tuning.MAINTAIN,
        warn: Callable[..., Any] = str,
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

    @property
    def allowslong(self: Self) -> bool:
        return self._data["allowslong"]

    @allowslong.setter
    def allowslong(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["allowslong"] = bool(value)

    @property
    def allowsshort(self: Self) -> bool:
        return self._data["allowsshort"]  # type: ignore[no-any-return]

    @allowsshort.setter
    def allowsshort(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["allowsshort"] = bool(value)

    @property
    def bundling(self: Self) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._data["bundling"]  # type: ignore[no-any-return]

    @bundling.setter
    def bundling(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["bundling"] = Tuning(value)

    def click(self: Self, cmd: Any = True, ctx: Any = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @property
    def expandsabbr(self: Self) -> bool:
        return self._data["expandsabbr"]  # type: ignore[no-any-return]

    @expandsabbr.setter
    def expandsabbr(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["expandsabbr"] = bool(value)

    @property
    def expectsabbr(self: Self) -> bool:
        return self._data["expectsabbr"]  # type: ignore[no-any-return]

    @expectsabbr.setter
    def expectsabbr(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["expectsabbr"] = bool(value)

    @property
    def expectsposix(self: Self) -> bool:
        return self._data["expectsposix"]  # type: ignore[no-any-return]

    @expectsposix.setter
    def expectsposix(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        if value == "infer":
            self._data["expectsposix"] = bool(
                os.environ.get("POSIXLY_CORRECT")
            )
        else:
            self._data["expectsposix"] = bool(value)

    @property
    def optdict(self: Self) -> Optdict:
        "This property gives a dictionary of options."
        return self._data["optdict"]  # type: ignore[no-any-return]

    @optdict.setter
    def optdict(self: Self, value: Any) -> None:
        dataA: Optdict
        self._data = getattr(self, "_data", dict())
        if "optdict" not in self._data.keys():
            self._data["optdict"] = Optdict()
        dataA = Optdict(value)
        self._data["optdict"].clear()
        self._data["optdict"].update(dataA)
        self._data["optdict"] = self._data["optdict"]

    def parse_args(
        self: Self,
        args: Iterable[Any] | None = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    @property
    def prog(self: Self) -> str:
        "This property represents the name of the program."
        return self._data["prog"]  # type: ignore[no-any-return]

    @prog.setter
    def prog(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        if value is None:
            self._data["prog"] = str(os.path.basename(sys.argv[0]))
        else:
            self._data["prog"] = str(value)

    @property
    def reconcilesorders(self: Self) -> bool:
        return self._data["reconcilesorders"]  # type: ignore[no-any-return]

    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["reconcilesorders"] = bool(value)

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
        return self._data["special"]  # type: ignore[no-any-return]

    @special.setter
    def special(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
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
    def warn(self: Self) -> types.FunctionType:
        "This property gives a function that takes in the warnings."
        return self._data["warn"]  # type: ignore[no-any-return]

    @warn.setter
    def warn(self: Self, value: Callable[..., Any]) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["warn"] = tofunc(value)

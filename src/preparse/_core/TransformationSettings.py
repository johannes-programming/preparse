from __future__ import annotations

__all__: list[str] = ["TransformationSettings"]

import os
import sys
from collections.abc import Callable
from typing import Any, Never, Self, cast

import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse.core.Click import Click
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from preparse.warnings.PreparseWarning import PreparseWarning


class TransformationSettings(Copyable):

    __slots__ = (
        "_bundling",
        "_expandsabbr",
        "_prog",
        "_reconcilesorders",
        "_special",
        "_warn",
    )

    _bundling: Tuning
    _expandsabbr: bool
    _prog: str
    _reconcilesorders: bool
    _special: Tuning
    _warn: Callable[[PreparseWarning], object]

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        bundling: int = Tuning.MAINTAIN,
        expandsabbr: SupportsBool = True,
        prog: object = None,
        reconcilesorders: SupportsBool = True,
        special: int = Tuning.MAINTAIN,
        warn: Callable[[PreparseWarning], object] = str,
    ) -> None:
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.prog = prog
        self.reconcilesorders = reconcilesorders
        self.special = special
        self.warn = warn

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def bundling(self: Self, /) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._bundling

    @bundling.setter
    def bundling(self: Self, value: int, /) -> None:
        "This property decides how to approach the bundling of short options."
        self._bundling = Tuning(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(**self.todict())

    @property
    def expandsabbr(self: Self, /) -> bool:
        return self._expandsabbr

    @expandsabbr.setter
    def expandsabbr(self: Self, value: SupportsBool, /) -> None:
        self._expandsabbr = bool(value)

    @property
    def prog(self: Self, /) -> str:
        "This property represents the name of the program."
        return self._prog

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        if value is None:
            self._prog = str(os.path.basename(sys.argv[0]))
        else:
            self._prog = str(value)

    @property
    def reconcilesorders(self: Self, /) -> bool:
        return self._reconcilesorders

    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: SupportsBool, /) -> None:
        self._reconcilesorders = bool(value)

    @property
    def special(self: Self, /) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return self._special

    @special.setter
    def special(self: Self, value: int, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        self._special = Tuning(value)

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        return dict(
            bundling=self.bundling,
            expandsabbr=self.expandsabbr,
            prog=self.prog,
            reconcilesorders=self.reconcilesorders,
            special=self.special,
            warn=self.warn,
        )

    @property
    def warn(self: Self, /) -> Callable[[PreparseWarning], object]:
        "This property gives a function that takes in the warnings."
        return self._warn

    @warn.setter
    def warn(
        self: Self,
        value: Callable[[PreparseWarning], object],
        /,
    ) -> None:
        "This property gives a function that takes in the warnings."
        self._warn = tofunc(value)

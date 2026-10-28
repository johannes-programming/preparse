from __future__ import annotations

__all__: list[str] = ["FrameworkSettings"]

import os
import sys
from typing import Any, Self

import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._core.no_change_setter import no_change_setter
from preparse.enums.Nargs import Nargs
from preparse.enums.NoChange import NoChange
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


class FrameworkSettings(Copyable):

    __slots__ = (
        "_allowslong",
        "_allowsshort",
        "_expectsabbr",
        "_expectsposix",
    )

    _allowslong: bool
    _allowsshort: bool
    _expectsabbr: bool
    _expectsposix: bool

    @setdoc.basic
    def __init__(
        self: Self,
        other: FrameworkSettings | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        allowslong: SupportsBool | NoChange = NoChange.NO_CHANGE,
        allowsshort: SupportsBool | NoChange = NoChange.NO_CHANGE,
        expectsabbr: SupportsBool | NoChange = NoChange.NO_CHANGE,
        expectsposix: SupportsBool | NoChange = NoChange.NO_CHANGE,
    ) -> None:
        self._allowslong = True
        self._allowsshort = True
        self._expectsabbr = True
        self._expectsposix = False
        self._init_other(other)
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @no_change_setter
    def _init_other(
        self: Self,
        other: FrameworkSettings,
    ) -> None:
        self._allowslong = other._allowslong
        self._allowsshort = other._allowsshort
        self._expectsabbr = other._expectsabbr
        self._expectsposix = other._expectsposix

    @property
    def allowslong(self: Self, /) -> bool:
        return self._allowslong

    @allowslong.setter
    @no_change_setter
    def allowslong(self: Self, value: SupportsBool, /) -> None:
        self._allowslong = bool(value)

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._allowsshort

    @allowsshort.setter
    @no_change_setter
    def allowsshort(self: Self, value: SupportsBool, /) -> None:
        self._allowsshort = bool(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def expectsabbr(self: Self, /) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    @no_change_setter
    def expectsabbr(self: Self, value: SupportsBool, /) -> None:
        self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._expectsposix

    @expectsposix.setter
    @no_change_setter
    def expectsposix(self: Self, value: SupportsBool, /) -> None:
        if value == "infer":
            self._expectsposix = bool(os.environ.get("POSIXLY_CORRECT"))
        else:
            self._expectsposix = bool(value)

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        return dict(
            allowslong=self.allowslong,
            allowsshort=self.allowsshort,
            expectsabbr=self.expectsabbr,
            expectsposix=self.expectsposix,
        )

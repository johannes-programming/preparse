from __future__ import annotations

__all__: list[str] = ["FrameworkSettings"]

import os
import sys
from enum import StrEnum
from typing import Any, Self

import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


class Infer(StrEnum):
    INFER = "infer"


class FrameworkSettings(Copyable):

    __slots__ = (
        "_allowslong",
        "_allowsshort",
        "_expectsabbr",
        "_expectsposix",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        other: FrameworkSettings | Infer = Infer.INFER,
        /,
        *,
        allowslong: SupportsBool | Infer = Infer.INFER,
        allowsshort: SupportsBool | Infer = Infer.INFER,
        expectsabbr: SupportsBool | Infer = Infer.INFER,
        expectsposix: SupportsBool | Infer = Infer.INFER,
    ) -> None:
        if isinstance(other, Infer) or not isinstance(allowslong, Infer):
            self.allowslong = allowslong
        else:
            self.allowslong = other.allowslong
        if isinstance(other, Infer) or not isinstance(allowsshort, Infer):
            self.allowsshort = allowsshort
        else:
            self.allowsshort = other.allowsshort
        if isinstance(other, Infer) or not isinstance(expectsabbr, Infer):
            self.expectsabbr = expectsabbr
        else:
            self.expectsabbr = other.expectsabbr
        if isinstance(other, Infer) or not isinstance(expectsposix, Infer):
            self.expectsposix = expectsposix
        else:
            self.expectsposix = other.expectsposix

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self, /) -> bool:
        return self._allowslong

    @allowslong.setter
    def allowslong(self: Self, value: SupportsBool | Infer, /) -> None:
        if isinstance(value, Infer):
            self._allowslong = True
        else:
            self._allowslong = bool(value)

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._allowsshort

    @allowsshort.setter
    def allowsshort(self: Self, value: SupportsBool | Infer, /) -> None:
        if isinstance(value, Infer):
            self._allowsshort = True
        else:
            self._allowsshort = bool(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def expectsabbr(self: Self, /) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    def expectsabbr(self: Self, value: SupportsBool, /) -> None:
        if isinstance(value, Infer):
            self._expectsabbr = True
        else:
            self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._expectsposix

    @expectsposix.setter
    def expectsposix(self: Self, value: SupportsBool | Infer, /) -> None:
        if isinstance(value, Infer) or value == "infer":
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

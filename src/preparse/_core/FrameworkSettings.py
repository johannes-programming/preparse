from __future__ import annotations

__all__: list[str] = ["FrameworkSettings"]

import os
import sys
from typing import Any, Self

import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


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
        other: FrameworkSettings | None = None,
        /,
        *,
        allowslong: SupportsBool | None = None,
        allowsshort: SupportsBool | None = None,
        expectsabbr: SupportsBool | None = None,
        expectsposix: SupportsBool | None = None,
    ) -> None:
        if allowslong is not None:
            self.allowslong = allowslong
        elif other is not None:
            self.allowslong = other.allowslong
        else:
            self.allowslong = True
        if allowsshort is not None:
            self.allowsshort = allowsshort
        elif other is not None:
            self.allowsshort = other.allowsshort
        else:
            self.allowsshort = True
        if expectsabbr is not None:
            self.expectsabbr = expectsabbr
        elif other is not None:
            self.expectsabbr = other.expectsabbr
        else:
            self.expectsabbr = True
        if expectsposix is not None:
            self.expectsposix = expectsposix
        elif other is not None:
            self.expectsposix = other.expectsposix
        else:
            self.expectsposix = False

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self, /) -> bool:
        return self._allowslong

    @allowslong.setter
    def allowslong(self: Self, value: SupportsBool, /) -> None:
        self._allowslong = bool(value)

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._allowsshort

    @allowsshort.setter
    def allowsshort(self: Self, value: SupportsBool, /) -> None:
        self._allowsshort = bool(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def expectsabbr(self: Self, /) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    def expectsabbr(self: Self, value: SupportsBool, /) -> None:
        self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._expectsposix

    @expectsposix.setter
    def expectsposix(self: Self, value: SupportsBool, /) -> None:
        value_: Any
        if value == "infer":
            value_ = os.environ.get("POSIXLY_CORRECT")
        else:
            value_ = value
        self._expectsposix = bool(value_)

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        return dict(
            allowslong=self.allowslong,
            allowsshort=self.allowsshort,
            expectsabbr=self.expectsabbr,
            expectsposix=self.expectsposix,
        )

from __future__ import annotations

__all__: list[str] = ["FrameworkSettings"]

import os
import sys
from typing import Any, Self

import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse.enums.Empty import Empty
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
        /,
        *,
        allowslong: SupportsBool | Empty = Empty.EMPTY,
        allowsshort: SupportsBool | Empty = Empty.EMPTY,
        expectsabbr: SupportsBool | Empty = Empty.EMPTY,
        expectsposix: SupportsBool | Empty = Empty.EMPTY,
    ) -> None:
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self, /) -> bool:
        return self._allowslong

    @allowslong.setter
    def allowslong(self: Self, value: SupportsBool | Empty, /) -> None:
        if isinstance(value, Empty):
            self._allowslong = True
        else:
            self._allowslong = bool(value)

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._allowsshort

    @allowsshort.setter
    def allowsshort(self: Self, value: SupportsBool | Empty, /) -> None:
        if isinstance(value, Empty):
            self._allowsshort = True
        else:
            self._allowsshort = bool(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(**self.todict())

    @property
    def expectsabbr(self: Self, /) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    def expectsabbr(self: Self, value: SupportsBool | Empty, /) -> None:
        if isinstance(value, Empty):
            self._expectsabbr = True
        else:
            self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._expectsposix

    @expectsposix.setter
    def expectsposix(self: Self, value: SupportsBool | Empty, /) -> None:
        if isinstance(value, Empty):
            self._expectsposix = False
        elif value == "infer":
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

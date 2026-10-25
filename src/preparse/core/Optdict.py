__all__: list[str] = ["Optdict"]

from collections.abc import Iterator
from typing import Any, Self

import cmp3
import datahold
import setdoc
from datarepr import datarepr
from frozendict import frozendict

from preparse.core.enums import Nargs, Tuning
from preparse.core.warnings import (
    PreparseAmbiguousOptionWarning,
    PreparseInvalidOptionWarning,
    PreparseRequiredArgumentWarning,
    PreparseUnallowedArgumentWarning,
    PreparseWarning,
)


class Optdict(cmp3.CmpABC, datahold.HoldDict[str, Nargs]):
    __slots__ = ()

    data: frozendict[str, Nargs]

    @setdoc.basic
    def __cmp__(self: Self, other: Any, /) -> int | None:
        if type(self) is type(other):
            return cmp3.cmp(self._data, other._data, mode="eq_strict")
        else:
            return cmp3.cmp(self._data, other, mode="eq_strict")

    __format__ = object.__format__

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, dict(self._data))

    __str__ = object.__str__

    @property
    def data(self: Self) -> frozendict[str, Nargs]:
        return frozendict[str, Nargs](self._data)

    @data.setter
    def data(self: Self, value: Any) -> None:
        a: frozendict[str, Nargs]
        x: Iterator[str]
        y: Iterator[Nargs]
        a = frozendict(value)
        x = map(str, a.keys())
        y = map(Nargs, a.values())
        self._data = frozendict[str, Nargs](zip(x, y, strict=True))

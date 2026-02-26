from typing import *

import cmp3
import datahold
import setdoc
from datarepr import datarepr
from frozendict import frozendict

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Optdict"]


class Optdict(cmp3.CmpABC, datahold.HoldDict):
    __slots__ = ()

    data: frozendict[str, Nargs]

    @setdoc.basic
    def __cmp__(self: Self, other: Any, /) -> Optional[int]:
        opp: Self
        if type(self) is type(other):
            opp = other
        else:
            try:
                opp = type(self)(other)
            except Exception:
                return
        return cmp3.cmp(self._data, opp._data, mode="eq_strict")

    __format__ = object.__format__

    @setdoc.basic
    def __init__(self: Self, data: Iterable = (), /, **kwargs: Any) -> None:
        self.data = dict(data, **kwargs)

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, dict(self._data))

    __str__ = object.__str__

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self.data)

    @property
    def data(self: Self) -> frozendict[str, Nargs]:
        return frozendict[str, Nargs](self._data)

    @data.setter
    def data(self: Self, value: Any) -> None:
        a: frozendict
        x: map
        y: map
        a = frozendict(value)
        x = map(str, a.keys())
        y = map(Nargs, a.values())
        self._data = frozendict[str, Nargs](zip(x, y, strict=True))

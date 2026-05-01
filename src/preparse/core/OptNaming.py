from typing import *

import datahold
import namings
import setdoc
from datarepr import datarepr

from preparse.enums.Nargs import Nargs

__all__ = ["OptNaming"]


class OptNaming(datahold.HoldNaming[Nargs]):
    __slots__ = ()

    data: namings.FrozenNaming[Nargs]

    def __eq__(self: Self, other: Any) -> bool:
        return type(self) is type(other) and self.data == other.data

    __format__ = object.__format__

    __ne__ = object.__ne__

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, dict(self._data))

    __str__ = object.__str__

    @property
    def data(self: Self) -> namings.FrozenNaming[Nargs]:
        return namings.FrozenNaming[Nargs](self._data)

    @data.setter
    def data(self: Self, value: Any) -> None:
        a: namings.FrozenNaming
        y: map
        a = namings.FrozenNaming(value)
        y = map(Nargs, a.values())
        self._data = namings.FrozenNaming[Nargs](zip(a.keys(), y, strict=True))

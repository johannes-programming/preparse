from typing import *

import datahold
import setdoc
from datarepr import datarepr
from namings import FrozenNaming

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["OptNaming"]


class OptNaming(datahold.HoldNaming[Nargs]):
    __slots__ = ()

    data: FrozenNaming[Nargs]

    @setdoc.basic
    def __eq__(self:Self, other:Any) -> bool:
        return type(self) is type(other) and self.data == other.data

    __format__ = object.__format__
    __ne__ = object.__ne__

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, dict(self))

    __str__ = object.__str__

    @property
    def data(self: Self) -> FrozenNaming[Nargs]:
        return FrozenNaming[Nargs](self._data)

    @data.setter
    def data(self: Self, value: Any) -> None:
        a: FrozenNaming
        a = FrozenNaming(value)
        self._data = FrozenNaming[Nargs](zip(a.keys(), map(Nargs, a.values())))

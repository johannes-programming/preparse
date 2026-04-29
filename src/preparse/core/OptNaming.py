from typing import *

import datahold
import setdoc

from preparse.core.enums import *
from preparse.core.warnings import *
from namings import FrozenNaming
from datarepr import datarepr


__all__ = ["OptNaming"]


class OptNaming(datahold.HoldNaming[Nargs]):
    __slots__ = ()

    data: FrozenNaming[Nargs]

    @setdoc.basic
    def __eq__(self:Self, other:Any)->bool:
        return type(self) is type(other) and self.data == other.data
    
    __ne__ = object.__ne__

    @setdoc.basic
    def __repr__(self:Self)->str:
        return datarepr(type(self).__name__, dict(self))

    @property
    def data(self: Self) -> FrozenNaming[Nargs]:
        return FrozenNaming[Nargs](self._data)

    @data.setter
    def data(self: Self, value: Any) -> None:
        a: FrozenNaming
        x: map
        y: map
        a = FrozenNaming(value)
        x = map(str, a.keys())
        y = map(Nargs, a.values())
        self._data = FrozenNaming[Nargs](zip(x, y, strict=True))

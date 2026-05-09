from typing import *

import datahold
import namings

from preparse.enums.Nargs import Nargs

__all__ = ["OptNaming"]


class OptNaming(datahold.HoldNaming[Nargs]):
    __slots__ = ()

    data: namings.FrozenNaming[Nargs]

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

import operator
from typing import *

import setdoc

from preparse._items.Item import Item
from preparse.core.enums import *

__all__ = ["Option"]


class Option(Item):

    __slots__ = ()

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.nargs == Nargs.REQUIRED_ARGUMENT)

    @property
    def joined(self: Self) -> bool:
        return self._joined

    @joined.setter
    def joined(self: Self, x: SupportsIndex) -> bool:
        self._joined = bool(operator.index(x))

    @property
    def nargs(self: Self) -> Nargs:
        return self._nargs

    @nargs.setter
    def nargs(self: Self, x: Any) -> None:
        self._nargs = Nargs(x)

    @property
    def right(self: Self) -> Optional[str]:
        return self._right

    @right.setter
    def right(self: Self, x: Any) -> None:
        if x is None:
            self._right = None
        else:
            self._right = str(x)

    @classmethod
    def sortkey(cls: type) -> int:
        return 0

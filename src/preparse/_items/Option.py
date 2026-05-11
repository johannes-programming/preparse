import operator
from typing import *

import setdoc

from preparse._items.Item import Item
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Option"]


class Option(Item):

    joined: bool
    nargs: Nargs
    right: Optional[str]

    __slots__ = ()

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.nargs == Nargs.REQUIRED_ARGUMENT)

    @property
    def joined(self: Self) -> bool:
        return self._data["joined"]

    @joined.setter
    def joined(self: Self, x: SupportsIndex) -> bool:
        self._data["joined"] = bool(operator.index(x))

    @property
    def nargs(self: Self) -> Nargs:
        return self._data["nargs"]

    @nargs.setter
    def nargs(self: Self, x: Any) -> None:
        self._data["nargs"] = Nargs(x)

    @property
    def right(self: Self) -> Optional[str]:
        return self._data["right"]

    @right.setter
    def right(self: Self, x: Any) -> None:
        if x is None:
            self._data["right"] = None
        else:
            self._data["right"] = str(x)

    @classmethod
    def sortkey(cls: type) -> int:
        return 0

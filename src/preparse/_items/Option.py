__all__: list[str] = ["Option"]

import operator
from typing import Self, SupportsIndex

from preparse._core.no_change_setter import no_change_setter
from preparse._items.Item import Item
from preparse.enums.Nargs import Nargs


class Option(Item):

    __slots__ = ()

    _joined: bool
    _nargs: Nargs
    _right: str | None

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.nargs == Nargs.REQUIRED_ARGUMENT)

    @property
    def joined(self: Self) -> bool:
        return self._joined

    @joined.setter
    @no_change_setter
    def joined(self: Self, x: SupportsIndex, /) -> None:
        self._joined = bool(operator.index(x))  # type: ignore[misc]

    @property
    def nargs(self: Self) -> Nargs:
        return self._nargs

    @nargs.setter
    @no_change_setter
    def nargs(self: Self, x: int, /) -> None:
        self._nargs = Nargs(x)  # type: ignore[misc]

    @property
    def right(self: Self) -> str | None:
        return self._right

    @right.setter
    @no_change_setter
    def right(self: Self, x: object, /) -> None:
        self._right = None if x is None else str(x)  # type: ignore[misc]

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 0

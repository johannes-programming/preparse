__all__: list[str] = ["Option"]

import operator
from typing import Optional, Self, SupportsIndex

from preparse._items.Item import Item


class Option(Item):

    __slots__ = ()

    _joined: bool
    _argmode: str
    _right: Optional[str]

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.argmode == ":")

    @property
    def joined(self: Self) -> bool:
        return self._joined

    @joined.setter
    def joined(self: Self, x: SupportsIndex, /) -> None:
        self._joined = bool(operator.index(x))  # type: ignore[misc]

    @property
    def argmode(self: Self) -> str:
        return self._argmode

    @argmode.setter
    def argmode(self: Self, value: str, /) -> None:
        self._argmode = value

    @property
    def right(self: Self) -> Optional[str]:
        return self._right

    @right.setter
    def right(self: Self, x: object, /) -> None:
        self._right = None if x is None else str(x)  # type: ignore[misc]

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 0

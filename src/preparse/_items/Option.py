__all__: list[str] = ["Option"]

import operator
from typing import Literal, Self, SupportsIndex

from preparse._items.Item import Item


class Option(Item):

    __slots__ = ()

    _joined: bool
    _argmode: Literal["", ":", "::"]
    _right: str | None

    def ishungry(self: Self, /) -> bool:
        return (self.right is None) and (self.argmode == ":")

    @property
    def joined(self: Self, /) -> bool:
        return self._joined

    @joined.setter
    def joined(self: Self, x: SupportsIndex, /) -> None:
        self._joined = bool(operator.index(x))  # type: ignore[misc]

    @property
    def argmode(self: Self, /) -> str:
        return self._argmode

    @argmode.setter
    def argmode(self: Self, value: Literal["", ":", "::"], /) -> None:
        self._argmode = value

    @property
    def right(self: Self, /) -> str | None:
        return self._right

    @right.setter
    def right(self: Self, x: object, /) -> None:
        self._right = None if x is None else str(x)  # type: ignore[misc]

    @staticmethod
    def sortkey() -> int:
        return 0

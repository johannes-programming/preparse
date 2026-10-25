__all__: list[str] = ["Option"]

import operator
from typing import Any, Self, SupportsIndex

from preparse._items.Item import Item
from preparse.core.enums import Nargs


class Option(Item):

    # joined: bool
    # nargs: Nargs
    # right: str | None

    __slots__ = ()

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.nargs == Nargs.REQUIRED_ARGUMENT)

    @property
    def joined(self: Self) -> bool:
        return self._data["joined"]  # type: ignore[no-any-return]

    @joined.setter
    def joined(self: Self, x: SupportsIndex) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["joined"] = bool(operator.index(x))

    @property
    def nargs(self: Self) -> Nargs:
        return self._data["nargs"]  # type: ignore[no-any-return]

    @nargs.setter
    def nargs(self: Self, x: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["nargs"] = Nargs(x)

    @property
    def right(self: Self) -> str | None:
        return self._data["right"]  # type: ignore[no-any-return]

    @right.setter
    def right(self: Self, x: Any) -> None:
        self._data = getattr(self, "_data", dict())
        if x is not None:
            self._data["right"] = str(x)
        else:
            self._data["right"] = None

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 0

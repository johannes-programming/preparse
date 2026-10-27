__all__: list[str] = ["Positional"]

from typing import Any, Self

import setdoc

from preparse._items.Item import Item
from preparse.core.enums import Nargs, Tuning


class Positional(Item):

    value: str

    __slots__ = ()

    @setdoc.basic
    def __init__(self: Self, value: Any) -> None:
        self.value = value

    def deparse(self: Self) -> list[str]:
        return [self.value]

    def isobvious(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 2

    @property
    def value(self: Self) -> str:
        return self._data["value"]

    @value.setter
    def value(self: Self, x: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["value"] = str(x)

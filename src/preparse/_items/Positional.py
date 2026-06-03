from typing import Any, Self

import setdoc

from preparse._items.Item import Item

__all__ = ["Positional"]


class Positional(Item):

    __slots__ = ("_value",)

    @setdoc.basic
    def __init__(self: Self, value: Any) -> None:
        self.value = value

    def deparse(self: Self) -> list[str]:
        return [self.value]

    @classmethod
    def getslotnames(cls: type[Self]) -> tuple[str, ...]:
        return ("_value",)

    def isobvious(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 2

    @property
    def value(self: Self) -> str:
        return self._value

    @value.setter
    def value(self: Self, x: object) -> None:
        self._value = str(x)

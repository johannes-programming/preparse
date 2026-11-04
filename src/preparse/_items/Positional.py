__all__: list[str] = ["Positional"]

from typing import Self

from preparse._items.Item import Item


class Positional(Item):

    __slots__ = ("_value",)

    def __init__(self: Self, /, value: str) -> None:
        self.value = value

    def deparse(self: Self, /) -> list[str]:
        return [self.value]

    def isobvious(self: Self, /) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @staticmethod
    def sortkey() -> int:
        return 2

    @property
    def value(self: Self, /) -> str:
        return self._value

    @value.setter
    def value(self: Self, x: object, /) -> None:
        self._value = str(x)

__all__: list[str] = ["Special"]

from typing import Self

from preparse._items.Item import Item


class Special(Item):

    __slots__ = ()

    def __init__(self: Self, /) -> None:
        pass

    def deparse(self: Self, /) -> list[str]:
        return ["--"]

    @staticmethod
    def sortkey() -> int:
        return 1

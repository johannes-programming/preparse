__all__: list[str] = ["Special"]

from typing import Self

import setdoc

from preparse._items.Item import Item


class Special(Item):

    __slots__ = ()

    @setdoc.basic
    def __init__(self: Self) -> None:
        pass

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def getslotnames(cls: type[Self]) -> tuple[str, ...]:
        return ()

    @classmethod
    def sortkey(cls: type) -> int:
        return 1

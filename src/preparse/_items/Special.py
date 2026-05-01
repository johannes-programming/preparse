from typing import *

from preparse._items.Item import Item
from preparse.core.enums import *

__all__ = ["Special"]


class Special(Item):

    __slots__ = ()

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 1

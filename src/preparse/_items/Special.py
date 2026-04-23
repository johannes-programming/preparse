from typing import *

from preparse._items.Item import Item
from preparse.enums import *

__all__ = ["Special"]


class Special(Item):

    __slots__ = ()

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def sortkey(cls: type) -> int:
        return 1

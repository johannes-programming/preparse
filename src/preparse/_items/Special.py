__all__: list[str] = ["Special"]

from typing import *

from preparse._items.Item import Item
from preparse.core.enums import *


class Special(Item):

    __slots__ = ()

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def sortkey(cls: type) -> int:
        return 1

from typing import *

import setdoc

from preparse._items.Item import Item
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Positional"]


class Positional(Item):

    value: str

    __slots__ = ()

    @setdoc.basic
    def __init__(self: Self, value: Any) -> None:
        self._data = dict()
        self.value = value

    def deparse(self: Self) -> list[str]:
        return [self.value]

    def isobvious(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @classmethod
    def sortkey(cls: type) -> int:
        return 2

    @property
    def value(self: Self) -> str:
        return self._data["value"]

    @value.setter
    def value(self: Self, x: Any) -> None:
        self._data["value"] = str(x)

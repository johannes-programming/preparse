from typing import *

from preparse._processing.items.Item import Item
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Positional"]


class Positional(Item):

    __slots__ = ()

    @dataprop
    def value(self: Self, x: Any) -> str:
        return str(x)

    #
    def __init__(self: Self, value: Any) -> None:
        self.value = value

    def deparse(self: Self) -> list[str]:
        return [self.value]

    def isobvious(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @classmethod
    def sortkey(cls: type) -> int:
        return 2

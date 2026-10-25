__all__: list[str] = ["Option"]

import operator
from typing import Any, Self, SupportsIndex

from preparse._items.Item import Item
from preparse._utils.dataprop import dataprop
from preparse.core.enums import Nargs, Tuning


class Option(Item):

    joined: bool
    nargs: Nargs
    right: str | None

    __slots__ = ()

    def ishungry(self: Self) -> bool:
        return (self.right is None) and (self.nargs == Nargs.REQUIRED_ARGUMENT)

    @dataprop
    def joined(self: Self, x: SupportsIndex) -> bool:
        return bool(operator.index(x))

    @dataprop
    def nargs(self: Self, x: Any) -> Nargs:
        return Nargs(x)

    @dataprop
    def right(self: Self, x: Any) -> str | None:
        if x is not None:
            return str(x)

    @classmethod
    def sortkey(cls: type[Self]) -> int:
        return 0

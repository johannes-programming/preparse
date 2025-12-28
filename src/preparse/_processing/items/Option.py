import operator
from typing import *

from preparse._processing.items.Item import Item
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Option"]


class Option(Item):

    joined: bool
    nargs: Nargs
    right: Optional[str]

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
    def right(self: Self, x: Any) -> Optional[str]:
        if x is not None:
            return str(x)

    @classmethod
    def sortkey(cls: type) -> int:
        return 0

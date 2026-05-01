import operator
from typing import *

import setdoc

from preparse._items.Option import Option
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Long"]


class Long(Option):

    abbr: str
    fullkey: str
    joined: bool
    nargs: Nargs
    right: Optional[str]

    __slots__ = ()

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        fullkey: str,
        joined: bool | str = False,
        right: Optional[str] = None,
    ) -> None:
        self.fullkey = fullkey
        self.joined = joined
        self.right = right

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.fullkey]
        elif self.joined:
            return [self.fullkey + "=" + self.right]
        else:
            return [self.fullkey, self.right]

    @dataprop
    def fullkey(self: Self, x: Any) -> str:
        return str(x)

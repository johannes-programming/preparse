import operator
from typing import *

import setdoc

from preparse._items.Option import Option
from preparse._utils.dataprop import dataprop
from preparse.enums import *

__all__ = ["Long"]


class Long(Option):

    abbr: str
    abbrlen: Optional[int]
    fullkey: str
    joined: bool
    minlen: Optional[int]
    nargs: Nargs
    right: Optional[str]

    __slots__ = ()

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        fullkey: str,
        abbrlen: Optional[int] = None,
        joined: bool | str = False,
        minlen: Optional[int] = None,
        right: Optional[str] = None,
    ) -> None:
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
        self.minlen = minlen
        self.right = right

    @property
    def abbr(self: Self) -> str:
        return self.fullkey[: self.abbrlen]

    @dataprop
    def abbrlen(self: Self, x: Optional[SupportsIndex]) -> Optional[int]:
        if x is not None:
            return operator.index(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.abbr]
        elif self.joined:
            return [self.abbr + "=" + self.right]
        else:
            return [self.abbr, self.right]

    @dataprop
    def fullkey(self: Self, x: Any) -> str:
        return str(x)
    
    @dataprop
    def minlen(self: Self, x: Optional[SupportsIndex]) -> Optional[int]:
        if x is not None:
            return operator.index(x)

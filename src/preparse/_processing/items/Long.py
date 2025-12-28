import operator
from typing import *

import setdoc

from preparse._processing.items.Option import Option
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Long"]


class Long(Option):

    abbr: str
    abbrlen: Optional[int]
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
        abbrlen: Optional[int] = None,
        joined: bool | str = False,
        right: Optional[str] = None,
    ) -> None:
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
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

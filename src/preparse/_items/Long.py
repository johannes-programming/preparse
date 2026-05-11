import operator
from typing import *

import setdoc

from preparse._items.Option import Option
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
        self._data: dict[str, Any] = dict()
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
        self.right = right

    @property
    def abbr(self: Self) -> str:
        return self.fullkey[: self.abbrlen]

    @property
    def abbrlen(self: Self) -> Optional[int]:
        return self._data["abbrlen"]

    @abbrlen.setter
    def abbrlen(self: Self, x: Optional[SupportsIndex]) -> None:
        if x is None:
            self._data["abbrlen"] = None
        else:
            self._data["abbrlen"] = operator.index(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.abbr]
        elif self.joined:
            return [self.abbr + "=" + self.right]
        else:
            return [self.abbr, self.right]

    @property
    def fullkey(self: Self) -> str:
        return self._data["fullkey"]

    @fullkey.setter
    def fullkey(self: Self, x: Any) -> None:
        self._data["fullkey"] = str(x)

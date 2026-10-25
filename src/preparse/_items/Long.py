__all__: list[str] = ["Long"]

import operator
from typing import Any, Self, SupportsIndex

import setdoc

from preparse._items.Option import Option
from preparse._utils.dataprop import dataprop
from preparse.core.enums import Nargs, Tuning


class Long(Option):

    abbr: str
    abbrlen: int | None
    fullkey: str
    joined: bool
    nargs: Nargs
    right: str | None

    __slots__ = ()

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        abbrlen: int | None = None,
        fullkey: str,
        joined: bool | str = False,
        right: str | None = None,
    ) -> None:
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
        self.right = right

    @property
    def abbr(self: Self) -> str:
        return self.fullkey[: self.abbrlen]

    @dataprop
    def abbrlen(self: Self, x: SupportsIndex | None) -> int | None:
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

__all__: list[str] = ["Long"]

import operator
from typing import Any, Self, SupportsIndex

import setdoc

from preparse._items.Option import Option
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

    @property
    def abbrlen(self: Self) -> int | None:
        return self._data["abbrlen"]

    @abbrlen.setter
    def abbrlen(self: Self, x: SupportsIndex | None) -> None:
        self._data = getattr(self, "_data", dict())
        if x is not None:
            self._data["abbrlen"] = operator.index(x)
        else:
            self._data["abbrlen"] = None

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
        self._data = getattr(self, "_data", dict())
        self._data["fullkey"] = str(x)

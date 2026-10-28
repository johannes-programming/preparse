__all__: list[str] = ["Long"]

import operator
from typing import Any, Self, SupportsIndex

import setdoc

from preparse._core.no_change_setter import no_change_setter
from preparse._items.Option import Option


class Long(Option):

    __slots__ = (
        "_nargs",
        "_joined",
        "_right",
        "_abbrlen",
        "_fullkey",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        abbrlen: int | None = None,
        fullkey: str,
        joined: bool = False,
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
        return self._abbrlen

    @abbrlen.setter
    @no_change_setter
    def abbrlen(self: Self, x: SupportsIndex | None) -> None:
        if x is None:
            self._abbrlen = None
        else:
            self._abbrlen = operator.index(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.abbr]
        elif self.joined:
            return [self.abbr + "=" + self.right]
        else:
            return [self.abbr, self.right]

    @property
    def fullkey(self: Self) -> str:
        return self._fullkey

    @fullkey.setter
    @no_change_setter
    def fullkey(self: Self, x: object) -> None:
        self._fullkey = str(x)

    @classmethod
    def getslotnames(cls: type[Self]) -> tuple[str, ...]:
        return (
            "_nargs",
            "_joined",
            "_right",
            "_abbrlen",
            "_fullkey",
        )

import operator
from typing import Any, Optional, Self, SupportsIndex

import setdoc

from preparse._items.Option import Option

__all__ = ["Long"]


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
        fullkey: str,
        abbrlen: Optional[int] = None,
        joined: bool = False,
        right: Optional[str] = None,
    ) -> None:
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
        self.right = right

    @property
    def abbr(self: Self) -> str:
        return self.fullkey[: self.abbrlen]

    @property
    def abbrlen(self: Self) -> Optional[int]:
        return self._abbrlen

    @abbrlen.setter
    def abbrlen(self: Self, x: Optional[SupportsIndex]) -> None:
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
    def fullkey(self: Self, x: Any) -> None:
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

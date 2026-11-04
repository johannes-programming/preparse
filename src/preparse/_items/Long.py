__all__: list[str] = ["Long"]

import operator
from typing import Literal, Self, SupportsIndex

from preparse._items.Option import Option


class Long(Option):

    __slots__ = (
        "_abbrlen",
        "_fullkey",
        "_joined",
        "_argmode",
        "_right",
    )

    def __init__(
        self: Self,
        /,
        *,
        abbrlen: int | None = None,
        argmode: Literal["", ":", "::"] = "",
        fullkey: str,
        joined: bool = False,
        right: str | None = None,
    ) -> None:
        self.abbrlen = abbrlen
        self.fullkey = fullkey
        self.joined = joined
        self.argmode = argmode
        self.right = right

    @property
    def abbr(self: Self) -> str:
        return self.fullkey[: self.abbrlen]

    @property
    def abbrlen(self: Self) -> int | None:
        return self._abbrlen

    @abbrlen.setter
    def abbrlen(self: Self, x: SupportsIndex | None, /) -> None:
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
    def fullkey(self: Self, x: object) -> None:
        self._fullkey = str(x)

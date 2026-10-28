__all__: list[str] = ["Long"]

import operator
from typing import Any, Optional, Self, SupportsIndex

import setdoc

from preparse._items.Option import Option
from preparse.enums.Nargs import Nargs


class Long(Option):

    __slots__ = (
        "_abbrlen",
        "_fullkey",
        "_joined",
        "_nargs",
        "_right",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        /,
        *,
        abbrlen: Optional[int] = None,
        fullkey: str,
        joined: bool = False,
        nargs: Nargs = Nargs.NO_ARGUMENT,
        right: Optional[str] = None,
    ) -> None:
        self.abbrlen = abbrlen
        self.fullkey = fullkey
        self.joined = joined
        self.nargs = nargs
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
    def fullkey(self: Self, x: object) -> None:
        self._fullkey = str(x)

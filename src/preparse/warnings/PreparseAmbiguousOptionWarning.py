from collections.abc import Iterable
from typing import Any, Self, cast

import setdoc

from preparse.warnings.PreparseLongonlyWarning import PreparseLongonlyWarning

__all__ = ["PreparseAmbiguousOptionWarning"]


class PreparseAmbiguousOptionWarning(PreparseLongonlyWarning):

    @setdoc.basic
    def __post_init__(
        self: Self,
        *,
        prog: Any,
        option: Any,
        possibilities: Iterable[object],
    ) -> None:
        self.prog = prog
        self.option = option
        self.possibilities = possibilities

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        ans: str
        x: Any
        ans = "option '%s' is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " '%s'" % x
        return ans

    @property
    def possibilities(self: Self) -> tuple[str, ...]:
        return cast(tuple[str, ...], self._data["possibilities"])

    @possibilities.setter
    def possibilities(self: Self, value: Iterable[object]) -> None:
        self._data["possibilities"] = tuple(map(str, value))

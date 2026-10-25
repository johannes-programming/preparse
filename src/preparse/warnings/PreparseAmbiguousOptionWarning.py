__all__: list[str] = ["PreparseAmbiguousOptionWarning"]

from collections.abc import Iterable
from typing import Any, Self, cast

import setdoc

from preparse.warnings.PreparseLongonlyWarning import PreparseLongonlyWarning


class PreparseAmbiguousOptionWarning(PreparseLongonlyWarning):

    @setdoc.basic
    def __post_init__(
        self: Self,
        *,
        option: object,
        possibilities: Iterable[object],
        prog: object,
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
    def possibilities(self: Self, value: Iterable[object], /) -> None:
        self._data["possibilities"] = tuple(map(str, value))

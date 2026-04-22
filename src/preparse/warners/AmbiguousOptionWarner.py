from abc import abstractmethod
from typing import *

import setdoc

from preparse._utils import *
from preparse.warners.LongonlyWarner import LongonlyWarner

__all__ = ["AmbiguousOptionWarner"]


class AmbiguousOptionWarner(LongonlyWarner):
    __slots__ = ()
    args: tuple[str]
    option: str
    possibilities: tuple[str, ...]
    prog: str

    @setdoc.basic
    def __init__(
        self: Self, *, prog: Any, option: Any, possibilities: Iterable
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

    @dataprop
    def possibilities(self: Self, value: Iterable) -> tuple[str, ...]:
        return tuple(map(str, value))

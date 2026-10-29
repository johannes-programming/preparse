from __future__ import annotations

__all__: list[str] = ["AmbiguousOptionMessage"]


from dataclasses import dataclass
from typing import Self

from preparse.messaging.Message import Message


@dataclass(eq=True)
class AmbiguousOptionMessage(Message):
    option: str
    possibilities: list[str]

    def oneliner(self: Self, /) -> str:
        ans: str
        ans = "option '%s' is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " '%s'" % x
        return ans

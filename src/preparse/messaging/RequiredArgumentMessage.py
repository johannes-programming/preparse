from __future__ import annotations

__all__: list[str] = ["RequiredArgumentMessage"]


from dataclasses import dataclass
from typing import Self

from preparse.messaging.Message import Message


@dataclass(eq=True)
class RequiredArgumentMessage(Message):
    option: str
    is_long: bool

    def oneliner(self: Self, /) -> str:
        return (
            "option '%s' requires an argument"
            if self.is_long
            else "option requires an argument -- '%s'"
        ) % self.option

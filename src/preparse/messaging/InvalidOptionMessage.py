from __future__ import annotations

__all__: list[str] = ["InvalidOptionMessage"]


from dataclasses import dataclass
from typing import Self

from preparse.messaging.Message import Message


@dataclass(eq=True)
class InvalidOptionMessage(Message):
    option: str
    is_long: bool

    def oneliner(self: Self, /) -> str:
        return (
            "unrecognized option '%s'"
            if self.is_long
            else "invalid option -- '%s'"
        ) % self.option

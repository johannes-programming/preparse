from __future__ import annotations

__all__: list[str] = ["UnallowedArgumentMessage"]


from dataclasses import dataclass
from typing import Self

from preparse.messaging.Message import Message


@dataclass(eq=True)
class UnallowedArgumentMessage(Message):
    option: str

    def oneliner(self: Self, /) -> str:
        return "option '%s' doesn't allow an argument" % self.option

from __future__ import annotations

__all__: list[str] = ["UnallowedArgumentMessage"]

from typing import Any, Self

from preparse.abc.Message import Message
from preparse.enum.NoChange import NoChange


class UnallowedArgumentMessage(Message):

    __slots__ = ("_option",)
    # option is always full key without value

    def __init__(
        self: Self,
        other: UnallowedArgumentMessage | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        option: object = NoChange.NO_CHANGE,
    ) -> None:
        if not isinstance(other, NoChange):
            self.option = other.option
        self.option = option

    def __str__(self: Self, /) -> str:
        "This method returns the core message."
        return f"option '{self.option}' doesn't allow an argument"

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            option=self.option,
        )

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        if isinstance(value, NoChange):
            return
        self._option = str(value)

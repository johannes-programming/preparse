from __future__ import annotations

__all__: list[str] = ["InvalidOptionMessage"]


from typing import Any, Self

from preparse.abc.Message import Message
from preparse.enum.NoChange import NoChange
from preparse.typing.SupportsBool import SupportsBool


class InvalidOptionMessage(Message):

    __slots__ = (
        "_is_long",
        "_option",
    )

    def __init__(
        self: Self,
        other: InvalidOptionMessage | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        is_long: SupportsBool | NoChange = NoChange.NO_CHANGE,
        option: object = NoChange.NO_CHANGE,
    ) -> None:
        if not isinstance(other, NoChange):
            self.option = other.option
            self.is_long = other.is_long
        self.option = option
        self.is_long = is_long

    def __str__(self: Self, /) -> str:
        "This method returns the core message."
        if self.is_long:
            return f"unrecognized option '{self.option}'"
        else:
            return f"invalid option -- '{self.option}'"

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            is_long=self.is_long,
            option=self.option,
        )

    @property
    def is_long(self: Self, /) -> bool:
        return self._is_long

    @is_long.setter
    def is_long(self: Self, value: SupportsBool | NoChange, /) -> None:
        if isinstance(value, NoChange):
            return
        self._is_long = bool(value)

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        if isinstance(value, NoChange):
            return
        self._option = str(value)

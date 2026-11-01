from __future__ import annotations

__all__: list[str] = ["InvalidOptionMessage"]


from typing import Any, Self

from preparse.abc.Message import Message
from preparse.typing import SupportsBool


class InvalidOptionMessage(Message):
    __slots__ = (
        "_is_long",
        "_option",
    )

    def __init__(
        self: Self,
        other: InvalidOptionMessage | None = None,
        /,
        *,
        is_long: SupportsBool = False,
        option: object = "",
    ) -> None:
        if isinstance(other, InvalidOptionMessage):
            self.option = other.option
            self.is_long = other.is_long
        self.option = option
        self.is_long = is_long

    def __str__(self: Self, /) -> str:
        return (
            "unrecognized option '%s'"
            if self.is_long
            else "invalid option -- '%s'"
        ) % self.option

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            is_long=self.is_long,
            option=self.option,
        )

    @property
    def is_long(self: Self, /) -> bool:
        return self._is_long

    @is_long.setter
    def is_long(self: Self, value: SupportsBool, /) -> None:
        self._is_long = bool(value)

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._option = str(value)

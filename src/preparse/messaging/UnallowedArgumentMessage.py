from __future__ import annotations

__all__: list[str] = ["UnallowedArgumentMessage"]

from typing import Self

from preparse.abc.Message import Message


class UnallowedArgumentMessage(Message):
    __slots__ = ("_option",)

    def __init__(
        self: Self,
        other: UnallowedArgumentMessage | None = None,
        /,
        *,
        option: object = "",
    ) -> None:
        if isinstance(other, UnallowedArgumentMessage):
            self.option = other.option
        self.option = str(option)

    def __str__(self: Self, /) -> str:
        return "option '%s' doesn't allow an argument" % self.option

    def _dict(self: Self, /) -> dict[str, str]:
        return dict(option=self.option)

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._option = str(value)

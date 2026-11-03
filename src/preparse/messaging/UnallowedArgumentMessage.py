__all__: list[str] = ["UnallowedArgumentMessage"]

from types import NotImplementedType
from typing import Any, Self

from preparse.abc.Message import Message


class UnallowedArgumentMessage(Message):

    __slots__ = ("_option",)
    # option is always full key without value

    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
        *,
        option: object = NotImplemented,
    ) -> None:
        if not isinstance(other, NotImplementedType):
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
        if isinstance(value, NotImplementedType):
            return
        self._option = str(value)

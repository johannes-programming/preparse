__all__: list[str] = ["DualMessage"]

from abc import abstractmethod
from types import NotImplementedType
from typing import Any, Self

from preparse.abc.Message import Message
from preparse.typing.SupportsBool import SupportsBool


class DualMessage(Message):

    __slots__ = (
        "_is_long",
        "_option",
    )

    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
        *,
        is_long: SupportsBool | NotImplementedType = NotImplemented,
        option: object = NotImplemented,
    ) -> None:
        if not isinstance(other, NotImplementedType):
            self.option = other.option
            self.is_long = other.is_long
        self.option = option
        self.is_long = is_long

    def __str__(self: Self, /) -> str:
        "This method returns the core message."
        if self.is_long:
            return self._longmsg() % self.option
        else:
            return self._shortmsg() % self.option

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            is_long=self.is_long,
            option=self.option,
        )

    @staticmethod
    @abstractmethod
    def _longmsg() -> str: ...

    @staticmethod
    @abstractmethod
    def _shortmsg() -> str: ...

    @property
    def is_long(self: Self, /) -> bool:
        return self._is_long

    @is_long.setter
    def is_long(self: Self, value: object, /) -> None:
        self._is_long = bool(value)

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._option = str(value)

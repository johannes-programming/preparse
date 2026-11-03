__all__: list[str] = ["DualMessage"]

from abc import abstractmethod
from types import NotImplementedType
from typing import Any, Self

from preparse.abc.Message import Message
from preparse.typing.SupportsBool import SupportsBool


class DualMessage(Message):

    __slots__ = (
        "_islong",
        "_option",
    )

    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
        *,
        islong: SupportsBool | NotImplementedType = NotImplemented,
        option: object = NotImplemented,
    ) -> None:
        if not isinstance(other, NotImplementedType):
            self.option = other.option
            self.islong = other.islong
        self.option = option
        self.islong = islong

    def __str__(self: Self, /) -> str:
        "This method returns the core message."
        if self.islong:
            return self._longmsg() % self.option
        else:
            return self._shortmsg() % self.option

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            islong=self.islong,
            option=self.option,
        )

    @staticmethod
    @abstractmethod
    def _longmsg() -> str: ...

    @staticmethod
    @abstractmethod
    def _shortmsg() -> str: ...

    @property
    def islong(self: Self, /) -> bool:
        return self._islong

    @islong.setter
    def islong(self: Self, value: object, /) -> None:
        self._islong = bool(value)

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._option = str(value)

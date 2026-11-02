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
        "_prog",
    )

    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
        *,
        islong: SupportsBool | NotImplementedType = NotImplemented,
        option: object = NotImplemented,
        prog: object = NotImplemented,
    ) -> None:
        if not isinstance(other, NotImplementedType):
            self.prog = other.prog
            self.option = other.option
            self.islong = other.islong
        self.prog = prog
        self.option = option
        self.islong = islong

    @staticmethod
    @abstractmethod
    def _longmsg() -> str: ...

    @staticmethod
    @abstractmethod
    def _shortmsg() -> str: ...

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return self._longmsg() % self.option
        else:
            return self._shortmsg() % self.option

    @property
    def islong(self: Self) -> bool:
        return self._islong

    @islong.setter
    def islong(self: Self, value: object, /) -> None:
        self._islong = bool(value)

    @property
    def option(self: Self) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._option = str(value)

    @property
    def prog(self: Self) -> str:
        return self._prog

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        self._prog = str(value)

    def todict(self: Self, /) -> dict[str, Any]:
        return dict(
            islong=self.islong,
            option=self.option,
            prog=self.prog,
        )

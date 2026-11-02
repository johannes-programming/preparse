__all__: list[str] = ["Message"]

from abc import abstractmethod
from types import NotImplementedType
from typing import Any, Self

from datarepr import datarepr

from preparse.abc.Copyable import Copyable


class Message(Copyable):

    __slots__ = ()

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, Message):
            return self.todict() == other.todict()
        else:
            return NotImplemented

    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    def __str__(self: Self, /) -> str:
        return f"{self.prog}: {self.getmsg()}"

    def copy(self: Self, /) -> Self:
        return type(self)(**self.todict())

    @abstractmethod
    def getmsg(self: Self, /) -> str: ...

    @property
    @abstractmethod
    def prog(self: Self, /) -> str: ...

    @abstractmethod
    def todict(self: Self) -> dict[str, Any]: ...

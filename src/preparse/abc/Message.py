__all__: list[str] = ["Message"]

import sys
from abc import abstractmethod
from types import NotImplementedType
from typing import Any, Self

from datarepr import datarepr

from preparse.abc.Copyable import Copyable


class Message(Copyable):

    __slots__ = ()

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, Message):
            return self._dict() == other._dict()
        else:
            return NotImplemented

    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self._dict())

    @abstractmethod
    def __str__(self: Self, /) -> str: ...

    @abstractmethod
    def _dict(self: Self, /) -> dict[str, Any]: ...

    def copy(self: Self, /) -> Self:
        return type(self)(**self._dict())

    def prog(self: Self, name: object, /) -> str:
        x: object
        x = sys.argv[0] if name is None else name
        return f"{x}: {self}"

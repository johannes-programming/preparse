from abc import abstractmethod
from types import NotImplementedType
from typing import Any, Self

from preparse.abc.Copyable import Copyable


class Representable(Copyable):
    __slots__ = ()

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, Representable):
            return self._dict() == other._dict()
        else:
            return NotImplemented

    def __repr__(self: Self, /) -> str:
        return f"{type(self).__name__}({self._dict()})"

    @abstractmethod
    def _dict(self: Self, /) -> dict[str, Any]: ...

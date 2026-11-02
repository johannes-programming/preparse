from __future__ import annotations

__all__: list[str] = ["Copyable"]

from abc import abstractmethod
from types import NotImplementedType
from typing import Self


class Copyable:

    __slots__ = ()

    @abstractmethod
    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
    ) -> None: ...

    def copy(self: Self, /) -> Self:
        return type(self)(self)

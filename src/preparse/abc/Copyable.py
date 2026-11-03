from __future__ import annotations

__all__: list[str] = ["Copyable"]

from abc import abstractmethod
from typing import Self

from preparse.enum.NoChange import NoChange


class Copyable:

    __slots__ = ()

    @abstractmethod
    def __init__(
        self: Self,
        other: Self | NoChange = NoChange.NO_CHANGE,
        /,
    ) -> None: ...

    def copy(self: Self, /) -> Self:
        return type(self)(self)

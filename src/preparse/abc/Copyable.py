"""Construction-based copying."""

from abc import ABC, abstractmethod
from typing import Self


class Copyable(ABC):
    __slots__ = ()

    @abstractmethod
    def __init__(self, other: Self | None = None, /) -> None: ...

    def copy(self: Self, /) -> Self:
        return type(self)(self)

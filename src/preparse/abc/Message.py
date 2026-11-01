"""Abstract diagnostic message."""

from abc import abstractmethod
from typing import Self

from .Representable import Representable


class Message(Representable):
    __slots__ = ()

    @abstractmethod
    def __str__(self: Self, /) -> str: ...

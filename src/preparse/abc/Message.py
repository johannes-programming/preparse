"""Abstract diagnostic message."""

from abc import abstractmethod
from typing import Self

from .Copyable import Copyable


class Message(Copyable):
    @abstractmethod
    def __str__(self: Self, /) -> str: ...

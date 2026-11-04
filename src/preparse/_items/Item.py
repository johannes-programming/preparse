__all__: list[str] = ["Item"]

from abc import ABC, abstractmethod
from typing import Any, Self


class Item(ABC):
    __slots__ = ()

    @abstractmethod
    def __init__(self: Self, /, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def deparse(self: Self, /) -> list[str]: ...

    @staticmethod
    @abstractmethod
    def sortkey() -> int: ...

__all__: list[str] = ["Item"]

from abc import ABC, abstractmethod
from typing import Any, Self

import setdoc


class Item(ABC):
    __slots__ = ()

    @abstractmethod
    @setdoc.basic
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abstractmethod
    def sortkey(cls: type[Self]) -> int: ...

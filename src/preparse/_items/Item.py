import abc
from typing import *

import setdoc
from copyable import Copyable

from preparse.core.enums import *

__all__ = ["Item"]


class Item(Copyable):
    __slots__ = ()

    @abc.abstractmethod
    @setdoc.basic
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None: ...

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def getslotnames(cls: type[Self]) -> tuple[str, ...]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type) -> int: ...

    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        x: str
        ans = dict()
        for x in self.getslotnames():
            ans[x] = getattr(self, x)
        return ans

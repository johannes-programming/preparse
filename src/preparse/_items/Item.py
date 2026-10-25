__all__: list[str] = ["Item"]

import abc
from typing import Any, Self

import setdoc
from copyable import Copyable

from preparse.core.enums import Nargs, Tuning


class Item(Copyable):
    __slots__ = ("_data",)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type[Self]) -> int: ...

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            ans = dict()
        else:
            ans = dict(ans)
        return ans

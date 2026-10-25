__all__: list[str] = ["Item"]

import abc
from typing import Self

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
    def sortkey(cls: type) -> int: ...

    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans: dict
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            ans = dict()
        else:
            ans = dict(ans)
        return ans

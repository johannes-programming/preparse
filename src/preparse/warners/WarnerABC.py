from abc import abstractmethod
from typing import *

import setdoc
from copyable import Copyable
from datarepr import datarepr

from preparse._utils import dataprop
from preparse.core.PreparseWarning import PreparseWarning

__all__ = ["WarnerABC"]


class WarnerABC(Copyable):
    __slots__ = ("_data",)
    args: tuple[str]
    option: str
    prog: str

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @setdoc.basic
    def __str__(self: Self) -> str:
        return f"{self.prog}: {self.getmsg()}"

    @property
    def args(self: Self) -> tuple[str]:
        "This property returns (str(self),)."
        return (str(self),)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @abstractmethod
    def getmsg(self: Self) -> str: ...

    @dataprop
    def option(self: Self, value: Any) -> str:
        return str(value)

    @dataprop
    def prog(self: Self, value: Any) -> str:
        return str(value)

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            return dict()
        else:
            return dict(ans)

    def warning(self: Self) -> PreparseWarning:
        return PreparseWarning(str(self))

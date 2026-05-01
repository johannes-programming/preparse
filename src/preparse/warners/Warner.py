from abc import abstractmethod
from typing import *

import namings
import setdoc
from copyable import Copyable
from datarepr import datarepr

from preparse._utils import *
from preparse.core.PreparseWarning import PreparseWarning

__all__ = ["Warner"]


class Warner(Copyable):
    __slots__ = ("_data",)
    option: str
    prog: str

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.toNaming())

    @setdoc.basic
    def __str__(self: Self) -> str:
        return f"{self.prog}: {self.getmsg()}"

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.toNaming())

    @abstractmethod
    def getmsg(self: Self) -> str: ...

    @dataprop
    def option(self: Self, value: Any) -> str:
        return str(value)

    @dataprop
    def prog(self: Self, value: Any) -> str:
        return str(value)

    def toNaming(self: Self) -> namings.Naming:
        "This method returns a naming representing the current instance."
        ans: namings.Naming
        try:
            ans = self._data
        except AttributeError:
            self._data = namings.Naming()
            return namings.Naming()
        else:
            return namings.Naming(ans)

    def warning(self: Self) -> PreparseWarning:
        return PreparseWarning(str(self))

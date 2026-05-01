import abc
from typing import *

import namings
import setdoc
from copyable import Copyable

from preparse.core.enums import *

__all__ = ["Item"]


class Item(Copyable):
    __slots__ = ("_data",)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.toNaming())

    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type) -> int: ...

    def toNaming(self: Self) -> namings.Naming:
        "This method returns a dict representing the current instance."
        ans: namings.Naming
        try:
            ans = self._data
        except AttributeError:
            self._data = namings.Naming()
            ans = namings.Naming()
        else:
            ans = namings.Naming(ans)
        return ans

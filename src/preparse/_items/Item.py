import abc
from typing import *

import setdoc
from copyable import Copyable

from preparse.core.enums import *
from namings import Naming

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

    def toNaming(self: Self) -> Naming:
        "This method returns a naming representing the current instance."
        ans: Naming
        try:
            ans = self._data
        except AttributeError:
            self._data = Naming()
            ans = Naming()
        else:
            ans = Naming(ans)
        return ans

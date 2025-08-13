import abc
import dataclasses
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Item"]


class BaseItem(abc.ABC):
    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...


@dataclasses.dataclass
class Item(BaseItem):
    key: Optional[str] = None
    remainder: bool | str = False
    value: Optional[str] = None

    def ishungry(self: Self) -> bool:
        return self.remainder and (self.value is None)

    def isoption(self: Self) -> bool:
        return self.key is not None

    def islong(self: Self) -> bool:
        return self.isoption() and self.key.startswith("-")

    def isbundle(self: Self) -> bool:
        return self.isoption() and not self.key.startswith("-")

    def isspecial(self: Self) -> bool:
        return self.key is None and self.value is None

    def ispositional(self: Self) -> bool:
        return self.key is None and self.value is not None

    def deparse(self: Self) -> list[str]:
        if self.isspecial():
            return ["--"]
        if self.ispositional():
            return [self.value]
        if self.isbundle():
            if self.value is None:
                return ["-" + self.key]
            if self.remainder:
                return ["-" + self.key + self.value]
            else:
                return ["-" + self.key, self.value]
        else:
            if self.value is None:
                return [self.key]
            if self.remainder:
                return [self.key + "=" + self.value]
            else:
                return [self.key, self.value]

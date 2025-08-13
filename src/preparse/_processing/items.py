import abc
import operator
from typing import *

import makeprop

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Item", "Option", "Special", "Positional"]


class Item(abc.ABC):
    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type) -> int: ...


class Option(Item):
    __slots__ = ("_key", "_remainder", "_value")

    def __init__(
        self: Self,
        *,
        key: str,
        remainder: bool | str = False,
        value: Optional[str] = None,
    ) -> None:
        self.key = key
        self.remainder = remainder
        self.value = value

    @makeprop.makeprop()
    def key(self: Self, x: Any) -> str:
        return str(x)

    @makeprop.makeprop()
    def remainder(self: Self, x: Any) -> bool | str:
        try:
            return bool(operator.index(x))
        except:
            return str(x)

    @makeprop.makeprop()
    def value(self: Self, x: Any) -> Optional[str]:
        if x is not None:
            return str(x)

    def ishungry(self: Self) -> bool:
        return self.remainder and (self.value is None)

    def islong(self: Self) -> bool:
        return self.key.startswith("-")

    def isbundle(self: Self) -> bool:
        return not self.key.startswith("-")

    def deparse(self: Self) -> list[str]:
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

    @classmethod
    def sortkey(cls: type) -> int:
        return 0


class Special(Item):
    __slots__ = ()

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def sortkey(cls: type) -> int:
        return 1


class Positional(Item):
    __slots__ = ("_value",)

    def __init__(self: Self, value: Any) -> None:
        self.value = value

    @makeprop.makeprop()
    def value(self: Self, x: Any) -> str:
        return str(x)

    def deparse(self: Self) -> list[str]:
        return [self.value]

    def isobvious(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    @classmethod
    def sortkey(cls: type) -> int:
        return 2

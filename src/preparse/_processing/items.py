import abc
import operator
from typing import *

import makeprop

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = [
    "Bundle",
    "Item",
    "Long",
    "Option",
    "Positional",
    "Special",
]


class Item(abc.ABC):
    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type) -> int: ...


class Positional(Item):
    __slots__ = ("_value",)
    value: str

    def __init__(self: Self, value: Any) -> None:
        self.value = value

    def iscomp(self: Self) -> bool:
        return self.value == "-" or not self.value.startswith("-")

    def deparse(self: Self) -> list[str]:
        return [self.value]

    @classmethod
    def sortkey(cls: type) -> int:
        return 2

    @makeprop.makeprop()
    def value(self: Self, x: Any) -> str:
        return str(x)


class Special(Item):
    __slots__ = ()

    def __init__(self: Self) -> None:
        pass

    def deparse(self: Self) -> list[str]:
        return ["--"]

    @classmethod
    def sortkey(cls: type) -> int:
        return 1


class Option(Item):
    @makeprop.makeprop()
    def joined(self: Self, x: Any) -> bool:
        return bool(x)

    @makeprop.makeprop()
    def right(self: Self, x: Any) -> Optional[str]:
        return str(x)

    @makeprop.makeprop()
    def nargs(self: Self, x: Any) -> Nargs:
        return Nargs(x)

    @classmethod
    def sortkey(cls: type) -> int:
        return 0


class Long(Option):
    __slots__ = ("_left", "_joined", "_right", "_nargs", "_abbrlen")

    def __init__(
        self: Self,
        *,
        left: Any,
        joined: Any = False,
        right: Any = None,
        nargs: Any = Nargs.NO_ARGUMENT,
        abbrlen: Optional[SupportsIndex] = None,
    ):
        self.left = left
        self.joined = joined
        self.right = right
        self.nargs = nargs
        self.abbrlen = abbrlen

    @makeprop.makeprop()
    def abbrlen(self: Self, x: Optional[SupportsIndex]) -> Optional[int]:
        if x is not None:
            return operator.index(x)

    @makeprop.makeprop()
    def left(self: Self, x: Any) -> str:
        return str(x).split("=")[0]

    @property
    def abbr(self: Self) -> str:
        return self.left[: self.abbrlen]

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.abbr]
        elif self.joined:
            return [self.abbr + "=" + self.right]
        else:
            return [self.abbr, self.right]


class Bundle(Option):
    __slots__ = ("_left", "_joined", "_right", "_nargs")

    def __init__(
        self: Self,
        *,
        left: Any,
        joined: Any = False,
        right: Any = None,
        nargs: Any = Nargs.NO_ARGUMENT,
    ):
        self.left = left
        self.joined = joined
        self.right = right
        self.nargs = nargs

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.left]
        elif self.joined:
            return [self.left + self.right]
        else:
            return [self.left, self.right]

    @makeprop.makeprop()
    def left(self: Self, x: Any) -> str:
        return str(x)

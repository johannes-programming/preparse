import abc
import operator
from typing import *

import makeprop

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Item", "Option", "Bundle", "Long", "Special", "Positional"]


class Item(abc.ABC):
    @abc.abstractmethod
    def deparse(self: Self) -> list[str]: ...

    @classmethod
    @abc.abstractmethod
    def sortkey(cls: type) -> int: ...


class Option(Item):

    def ishungry(self: Self) -> bool:
        return self.joined and (self.right is None)

    @classmethod
    def sortkey(cls: type) -> int:
        return 0


class Bundle(Option):
    __slots__ = ("_chars", "_joined", "_right")

    def __init__(
        self: Self,
        *,
        chars: str,
        joined: bool | str = False,
        right: Optional[str] = None,
    ) -> None:
        self.chars = chars
        self.joined = joined
        self.right = right

    @classmethod
    def _split_allowslong(cls: type, chars: str) -> list[str]:
        ans: list[str] = list()
        x: str
        for x in chars:
            if x == "-":
                ans[-1].chars += "-"
            else:
                ans.append(x)
        return ans

    @classmethod
    def _split_shortonly(cls: type, chars: str) -> list[str]:
        raise NotImplementedError

    @makeprop.makeprop()
    def chars(self: Self, x: Any) -> str:
        return str(x)

    @makeprop.makeprop()
    def joined(self: Self, x: SupportsIndex) -> bool:
        return bool(operator.index(x))

    @makeprop.makeprop()
    def right(self: Self, x: Any) -> Optional[str]:
        if x is not None:
            return str(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return ["-" + self.chars]
        if self.joined:
            return ["-" + self.chars + self.right]
        else:
            return ["-" + self.chars, self.right]

    def split(self: Self, *, allowslong: bool) -> list[Item]:
        parts: list[str]
        if allowslong:
            parts = self._split_allowslong(self.chars)
        else:
            parts = self._split_shortonly(self.chars)
        ans: list[Self] = list()
        x: str
        for x in parts:
            ans.append(Bundle(chars=x))
        self.chars = ans[-1].chars
        ans[-1] = self
        return ans


class Long(Option):
    __slots__ = ("_fullkey", "_abbrlen", "_joined", "_right")

    def __init__(
        self: Self,
        *,
        fullkey: str,
        abbrlen: Optional[int] = None,
        joined: bool | str = False,
        right: Optional[str] = None,
    ) -> None:
        self.fullkey = fullkey
        self.abbrlen = abbrlen
        self.joined = joined
        self.right = right

    @makeprop.makeprop()
    def fullkey(self: Self, x: Any) -> str:
        return str(x)

    @makeprop.makeprop()
    def abbrlen(self: Self, x: Optional[SupportsIndex]) -> Optional[int]:
        if x is not None:
            return operator.index(x)

    @makeprop.makeprop()
    def joined(self: Self, x: Any) -> bool | str:
        try:
            return bool(operator.index(x))
        except:
            return str(x)

    @makeprop.makeprop()
    def right(self: Self, x: Any) -> Optional[str]:
        if x is not None:
            return str(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return [self.fullkey]
        if self.joined:
            return [self.fullkey + "=" + self.right]
        else:
            return [self.fullkey, self.right]


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

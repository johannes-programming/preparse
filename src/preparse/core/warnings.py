from abc import abstractmethod
from typing import *

import setdoc
from copyable import Copyable
from datarepr import datarepr

from preparse._utils import *

__all__ = [
    "PreparseAmbiguousOptionWarning",
    "PreparseInvalidOptionWarning",
    "PreparseRequiredArgumentWarning",
    "PreparseUnallowedArgumentWarning",
    "PreparseWarning",
]


class PreparseWarning(Warning, Copyable):

    _data: dict[str, Any]

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @setdoc.basic
    def __str__(self: Self) -> str:
        return f"{self.prog}: {self.getmsg()}"

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

    def todict(self: Self) -> dict:
        "This method returns a dict representing the current instance."
        ans: dict
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            return dict()
        else:
            return dict(ans)


class PreparseDualWarning(PreparseWarning):

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any, islong: Any) -> None:
        self.prog = prog
        self.option = option
        self.islong = islong

    @classmethod
    @abstractmethod
    def _longmsg(cls: type[Self]) -> str: ...

    @classmethod
    @abstractmethod
    def _shortmsg(cls: type[Self]) -> str: ...

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return self._longmsg() % self.option
        else:
            return self._shortmsg() % self.option

    @dataprop
    def islong(self: Self, value: Any) -> bool:
        return bool(value)


class PreparseInvalidOptionWarning(PreparseDualWarning):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "unrecognized option '%s'"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "invalid option -- '%s'"


class PreparseRequiredArgumentWarning(PreparseDualWarning):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "option '%s' requires an argument"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "option requires an argument -- '%s'"


class PreparseLongonlyWarning(PreparseWarning):
    pass  # only possible for long options


class PreparseAmbiguousOptionWarning(PreparseLongonlyWarning):

    @setdoc.basic
    def __init__(
        self: Self, *, prog: Any, option: Any, possibilities: Iterable
    ) -> None:
        self.prog = prog
        self.option = option
        self.possibilities = possibilities

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        ans: str
        x: Any
        ans = "option '%s' is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " '%s'" % x
        return ans

    @dataprop
    def possibilities(self: Self, value: Iterable) -> tuple[str, ...]:
        return tuple(map(str, value))


class PreparseUnallowedArgumentWarning(PreparseLongonlyWarning):

    # option is always full key without value

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

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

    args: tuple[str]
    option: str
    prog: str

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any, islong: Any) -> None:
        self.prog = prog
        self.option = option
        self.islong = islong

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return type(self)._longmsg % self.option
        else:
            return type(self)._shortmsg % self.option

    @dataprop
    def islong(self: Self, value: Any) -> bool:
        return bool(value)


class PreparseInvalidOptionWarning(PreparseDualWarning):
    args: tuple[str]
    option: str
    prog: str
    _longmsg = "unrecognized option '%s'"
    _shortmsg = "invalid option -- '%s'"


class PreparseRequiredArgumentWarning(PreparseDualWarning):
    args: tuple[str]
    option: str
    prog: str
    _longmsg = "option '%s' requires an argument"
    _shortmsg = "option requires an argument -- '%s'"


class PreparseLongonlyWarning(PreparseWarning):
    args: tuple[str]
    option: str
    prog: str
    # only possible for long options


class PreparseAmbiguousOptionWarning(PreparseLongonlyWarning):
    args: tuple[str]
    option: str
    possibilities: tuple[str, ...]
    prog: str

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
    args: tuple[str]
    option: str
    prog: str
    # option is always full key without value

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

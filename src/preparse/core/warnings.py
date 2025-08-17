import abc
from typing import *

from preparse._processing.utils import *

__all__ = [
    "PreparseAmbiguousOptionWarning",
    "PreparseInvalidOptionWarning",
    "PreparseRequiredArgumentWarning",
    "PreparseUnallowedArgumentWarning",
    "PreparseWarning",
]


class PreparseWarning(Warning, metaclass=abc.ABCMeta):
    @dataprop
    def prog(self: Self, value: Any) -> str:
        return str(value)

    @dataprop
    def option(self: Self, value: Any) -> str:
        return str(value)

    __slots__ = "_data"

    def __str__(self: Self) -> str:
        "This magic method implements str(self)."
        return f"{self.prog}: {self.getmsg()}"

    @property
    def args(self: Self):
        "This property returns (str(self),)."
        return (str(self),)

    @abc.abstractmethod
    def getmsg(self: Self) -> str: ...


class PreparseAmbiguousOptionWarning(PreparseWarning):
    # only possible with long options

    @dataprop
    def possibilities(self: Self, value: Iterable) -> tuple[str]:
        l: list = list(value)
        i: int
        for i in range(len(l)):
            l[i] = str(l[i])
        ans: tuple[str] = tuple(l)
        return ans

    def __init__(
        self: Self, *, prog: Any, option: Any, possibilities: Iterable
    ) -> None:
        "This magic method initializes the current instance."
        self.prog = prog
        self.option = option
        self.possibilities = possibilities

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        ans = "option %r is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " %r" % x
        return ans


class PreparseInvalidOptionWarning(PreparseWarning):

    @dataprop
    def islong(self: Self, value: Any) -> bool:
        return bool(value)

    def __init__(self: Self, *, prog: Any, option: Any, islong: Any) -> None:
        "This magic method initializes the current instance."
        self.prog = prog
        self.option = option
        self.islong = islong

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return "unrecognized option %r" % self.option
        else:
            return "invalid option -- %r" % self.option


class PreparseRequiredArgumentWarning(PreparseWarning):

    @dataprop
    def islong(self: Self, value: Any) -> bool:
        return bool(value)

    def __init__(self: Self, *, prog: Any, option: Any, islong: Any) -> None:
        "This magic method initializes the current instance."
        self.prog = prog
        self.option = option
        self.islong = islong

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return "option %r requires an argument" % self.option
        else:
            return "option requires an argument -- %r" % self.option


class PreparseUnallowedArgumentWarning(PreparseWarning):
    # only possible for long options
    # option is always full key without value

    def __init__(self: Self, *, prog: Any, option: Any) -> None:
        "This magic method initializes the current instance."
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option %r doesn't allow an argument" % self.option

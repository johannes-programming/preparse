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
    def __init__(self: Self, **kwargs: Any) -> None:
        "This magic method initializes the current instance."
        for n in type(self).__slots__:
            setattr(self, n, kwargs.pop(n))
        for k, v in kwargs.items():
            setattr(self, k, v)

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
    __slots__ = ("prog", "option", "possibilities")

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        ans = "option %r is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " %r" % x
        return ans


class PreparseInvalidOptionWarning(PreparseWarning):
    __slots__ = ("prog", "option", "islong")

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return "unrecognized option %r" % self.option
        else:
            return "invalid option -- %r" % self.option


class PreparseRequiredArgumentWarning(PreparseWarning):
    __slots__ = ("prog", "option", "islong")

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return "option %r requires an argument" % self.option
        else:
            return "option requires an argument -- %r" % self.option


class PreparseUnallowedArgumentWarning(PreparseWarning):
    # only possible for long options
    # option is always full key without value
    __slots__ = ("prog", "option")

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option %r doesn't allow an argument" % self.option

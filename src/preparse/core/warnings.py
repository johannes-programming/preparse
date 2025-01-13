import enum
import sys
from typing import *

__all__ = [
    "PreparseAmbiguousOptionWarning",
    "PreparseInvalidOptionWarning",
    "PreparseRequiredArgumentWarning",
    "PreparseUnallowedArgumentWarning",
    "PreparseUnrecognizedOptionWarning",
    "PreparseWarning",
    "doNothing",
]


class PreparseWarning(Warning):
    def __init__(self, **kwargs: Any) -> None:
        "This magic method initializes the current instance."
        for n in type(self).__slots__:
            setattr(self, n, kwargs.pop(n))
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        "This magic method returns str(self)."
        return f"{self.prog}: {self.getmsg()}"

    @property
    def args(self):
        "This property returns (str(self),)."
        return (str(self),)

    def getmsg(self) -> str:
        raise NotImplementedError


class PreparseAmbiguousOptionWarning(PreparseWarning):
    __slots__ = ("prog", "option", "possibilities")

    def getmsg(self) -> str:
        ans = "option %r is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " %r" % x
        return ans


class PreparseInvalidOptionWarning(PreparseWarning):
    __slots__ = ("prog", "option")

    def getmsg(self) -> str:
        return "invalid option -- %r" % self.option


class PreparseRequiredArgumentWarning(PreparseWarning):
    __slots__ = ("prog", "option")

    def getmsg(self) -> str:
        return "option requires an argument -- %r" % self.option


class PreparseUnallowedArgumentWarning(PreparseWarning):
    __slots__ = ("prog", "option")

    def getmsg(self) -> str:
        return "option %r doesn't allow an argument" % self.option


class PreparseUnrecognizedOptionWarning(PreparseWarning):
    __slots__ = ("prog", "option")

    def getmsg(self) -> str:
        return "unrecognized option %r" % self.option


def doNothing(*args: Any, **kwargs: Any) -> None:
    "This function does nothing."
    return

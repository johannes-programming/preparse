__all__: list[str] = [
    "PreparseAmbiguousOptionWarning",
    "PreparseInvalidOptionWarning",
    "PreparseRequiredArgumentWarning",
    "PreparseUnallowedArgumentWarning",
    "PreparseWarning",
]

from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Self

import setdoc
from copyable import Copyable
from datarepr import datarepr


class PreparseWarning(Warning, Copyable):

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @setdoc.basic
    def __str__(self: Self) -> str:
        return f"{self.prog}: {self.getmsg()}"

    @property
    def args(self: Self) -> tuple[str]:  # type: ignore[override]
        "This property returns (str(self),)."
        return (str(self),)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @abstractmethod
    def getmsg(self: Self) -> str: ...

    @property
    def option(self: Self) -> str:
        return self._data["option"]

    @option.setter
    def option(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["option"] = str(value)

    @property
    def prog(self: Self) -> str:
        return self._data["prog"]  # type: ignore[no-any-return]

    @prog.setter
    def prog(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["prog"] = str(value)

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        try:
            ans = self._data
        except AttributeError:
            self._data = dict()
            return dict()
        else:
            return dict(ans)


class PreparseDualWarning(PreparseWarning):

    @setdoc.basic
    def __init__(self: Self, *, islong: Any, option: Any, prog: Any) -> None:
        self.prog = prog
        self.option = option
        self.islong = islong

    @staticmethod
    @abstractmethod
    def _longmsg() -> str: ...
    @staticmethod
    @abstractmethod
    def _shortmsg() -> str: ...

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return self._longmsg() % self.option
        else:
            return self._shortmsg() % self.option

    @property
    def islong(self: Self) -> bool:
        return self._data["islong"]  # type: ignore[no-any-return]

    @islong.setter
    def islong(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["islong"] = bool(value)


class PreparseInvalidOptionWarning(PreparseDualWarning):
    @staticmethod
    def _longmsg() -> str:
        return "unrecognized option '%s'"

    @staticmethod
    def _shortmsg() -> str:
        return "invalid option -- '%s'"


class PreparseRequiredArgumentWarning(PreparseDualWarning):

    @staticmethod
    def _longmsg() -> str:
        return "option '%s' requires an argument"

    @staticmethod
    def _shortmsg() -> str:
        return "option requires an argument -- '%s'"


class PreparseLongonlyWarning(PreparseWarning):
    pass
    # only possible for long options


class PreparseAmbiguousOptionWarning(PreparseLongonlyWarning):

    @setdoc.basic
    def __init__(
        self: Self, *, option: Any, possibilities: Iterable[Any], prog: Any
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

    @property
    def possibilities(self: Self) -> tuple[str, ...]:
        return self._data["possibilities"]  # type: ignore[no-any-return]

    @possibilities.setter
    def possibilities(self: Self, value: Iterable[Any]) -> None:
        self._data = getattr(self, "_data", dict())
        self._data["possibilities"] = tuple(map(str, value))


class PreparseUnallowedArgumentWarning(PreparseLongonlyWarning):

    # option is always full key without value

    @setdoc.basic
    def __init__(self: Self, *, option: Any, prog: Any) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

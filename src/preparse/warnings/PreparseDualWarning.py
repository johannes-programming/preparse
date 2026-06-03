from abc import abstractmethod
from typing import Any, Self, cast

import setdoc

from preparse.warnings.PreparseWarning import PreparseWarning

__all__ = ["PreparseDualWarning"]


class PreparseDualWarning(PreparseWarning):

    @setdoc.basic
    def __post_init__(
        self: Self, *, prog: Any, option: Any, islong: Any
    ) -> None:
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

    @property
    def islong(self: Self) -> bool:
        return cast(bool, self._data["islong"])

    @islong.setter
    def islong(self: Self, value: Any) -> None:
        self._data["islong"] = bool(value)

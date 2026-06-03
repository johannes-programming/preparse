from abc import abstractmethod
from typing import Any, Self, cast

import setdoc
from copyable import Copyable
from datarepr import datarepr

__all__ = ["PreparseWarning"]


class PreparseWarning(Warning, Copyable):

    _data: dict[str, Any]

    @setdoc.basic
    def __init__(self: Self, **kwargs: Any) -> None:
        Warning.__init__(self)
        self._data = dict()
        self.__post_init__(**kwargs)

    @abstractmethod
    @setdoc.basic
    def __post_init__(self: Self, **kwargs: Any) -> None: ...

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

    @property
    def option(self: Self) -> str:
        return cast(str, self._data["option"])

    @option.setter
    def option(self: Self, value: object, /) -> None:
        self._data["option"] = str(value)

    @property
    def prog(self: Self) -> str:
        return cast(str, self._data["prog"])

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
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

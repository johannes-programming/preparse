__all__: list[str] = ["AmbiguousOptionMessage"]

from collections.abc import Iterable
from types import NotImplementedType
from typing import Any, Self

import setdoc

from preparse.abc.Message import Message


class AmbiguousOptionMessage(Message):

    __slots__ = (
        "_option",
        "_possibilities",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        other: Self | NotImplementedType = NotImplemented,
        /,
        *,
        option: object = NotImplemented,
        possibilities: Iterable[object] | NotImplementedType = NotImplemented,
    ) -> None:
        if not isinstance(other, NotImplementedType):
            self.option = other.option
            self.possibilities = other.possibilities
        self.option = option
        self.possibilities = possibilities

    def __str__(self: Self, /) -> str:
        "This method returns the core message."
        ans: str
        x: Any
        ans = f"option '{self.option}' is ambiguous; possibilities:"
        for x in self.possibilities:
            ans += f" '{x}'"
        return ans

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            option=self.option,
            possibilities=self.possibilities,
        )

    @property
    def option(self: Self, /) -> str:
        return self._option

    @option.setter
    def option(self: Self, value: object, /) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._option = str(value)

    @property
    def possibilities(self: Self, /) -> tuple[str, ...]:
        return self._possibilities

    @possibilities.setter
    def possibilities(self: Self, value: Iterable[object], /) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._possibilities = tuple(map(str, value))

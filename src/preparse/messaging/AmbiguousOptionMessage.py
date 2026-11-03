from __future__ import annotations

__all__: list[str] = ["AmbiguousOptionMessage"]

from collections.abc import Iterable
from typing import Any, Self

import setdoc

from preparse.abc.Message import Message
from preparse.enum.NoChange import NoChange


class AmbiguousOptionMessage(Message):

    __slots__ = (
        "_option",
        "_possibilities",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        other: AmbiguousOptionMessage | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        option: object = NoChange.NO_CHANGE,
        possibilities: Iterable[object] | NoChange = NoChange.NO_CHANGE,
    ) -> None:
        if not isinstance(other, NoChange):
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
        if isinstance(value, NoChange):
            return
        self._option = str(value)

    @property
    def possibilities(self: Self, /) -> tuple[str, ...]:
        return self._possibilities

    @possibilities.setter
    def possibilities(
        self: Self, value: Iterable[object] | NoChange, /
    ) -> None:
        if isinstance(value, NoChange):
            return
        self._possibilities = tuple(map(str, value))

from __future__ import annotations

__all__: list[str] = ["AmbiguousOptionMessage"]

from collections.abc import Iterable
from typing import Any, Self

from preparse.abc.Message import Message


class AmbiguousOptionMessage(Message):
    __slots__ = ("_option", "_possibilities")

    def __init__(
        self,
        other: AmbiguousOptionMessage | None = None,
        /,
        *,
        option: object = "",
        possibilities: Iterable[object] = (),
    ) -> None:
        if isinstance(other, AmbiguousOptionMessage):
            self.option = other.option
            self.possibilities = other.possibilities
        self.option = option
        self.possibilities = possibilities

    def __str__(self: Self, /) -> str:
        ans = "option '%s' is ambiguous; possibilities:" % self.option
        for x in self.possibilities:
            ans += " '%s'" % x
        return ans

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AmbiguousOptionMessage) and (
            self.option,
            self.possibilities,
        ) == (other.option, other.possibilities)

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
        self._option = str(value)

    @property
    def possibilities(self: Self, /) -> tuple[str, ...]:
        return self._possibilities

    @possibilities.setter
    def possibilities(self: Self, value: Iterable[object], /) -> None:
        self._possibilities = tuple(str(x) for x in value)

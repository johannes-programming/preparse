from __future__ import annotations

__all__: list[str] = ["AmbiguousOptionMessage"]

from collections.abc import Iterable
from typing import Any, Self

from preparse.abc.Message import Message


class AmbiguousOptionMessage(Message):
    __slots__ = ("_option", "_possibilities")

    def __init__(
        self: Self,
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
        ans: str
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
        self._option = str(value)

    @property
    def possibilities(self: Self, /) -> tuple[str, ...]:
        return self._possibilities

    @possibilities.setter
    def possibilities(self: Self, value: Iterable[object], /) -> None:
        self._possibilities = tuple(str(x) for x in value)

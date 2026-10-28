__all__: list[str] = ["no_change_setter"]

from collections.abc import Callable
from typing import TypeVar

from preparse.enums.NoChange import NoChange

Self_ = TypeVar("Self_")
Value = TypeVar("Value")


def no_change_setter(
    old: Callable[[Self_, Value], object], /
) -> Callable[[Self_, Value | NoChange], None]:
    def new(self: Self_, value: Value | NoChange, /) -> None:
        if not isinstance(value, NoChange):
            old(self, value)

    return new

__all__: list[str] = ["no_change_setter"]

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from preparse.enums.NoChange import NoChange

Self_ = TypeVar("Self_")
Value = TypeVar("Value")


def no_change_setter(
    old: Callable[[Self_, Value | NoChange], object], /
) -> Callable[[Self_, Value], None]:
    @wraps(old)
    def new(self: Self_, value: Value, /) -> None:
        if not isinstance(value, NoChange):
            old(self, value)

    return new

from typing import Self

from preparse.abc.Message import Message


class RequiredArgumentMessage(Message):
    def __init__(self, option: object = "", is_long: object = False) -> None:
        if isinstance(option, RequiredArgumentMessage):
            other = option
            option, is_long = other.option, other.is_long
        self.option = str(option)
        self.is_long = bool(is_long)

    def __str__(self: Self, /) -> str:
        return (
            "option '%s' requires an argument"
            if self.is_long
            else "option requires an argument -- '%s'"
        ) % self.option

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RequiredArgumentMessage) and (
            self.option,
            self.is_long,
        ) == (other.option, other.is_long)

    def __repr__(self) -> str:
        return f"RequiredArgumentMessage({self.option!r}, {self.is_long!r})"

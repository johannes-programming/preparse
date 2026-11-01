from typing import Self

from preparse.abc.Message import Message


class InvalidOptionMessage(Message):
    def __init__(self, option: object = "", is_long: object = False) -> None:
        if isinstance(option, InvalidOptionMessage):
            other = option
            option, is_long = other.option, other.is_long
        self.option = str(option)
        self.is_long = bool(is_long)

    def __str__(self: Self, /) -> str:
        return (
            "unrecognized option '%s'"
            if self.is_long
            else "invalid option -- '%s'"
        ) % self.option

    def __eq__(self, other: object) -> bool:
        return isinstance(other, InvalidOptionMessage) and (
            self.option,
            self.is_long,
        ) == (other.option, other.is_long)

    def __repr__(self) -> str:
        return f"InvalidOptionMessage({self.option!r}, {self.is_long!r})"

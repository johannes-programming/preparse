from typing import Self

from preparse.abc.Message import Message


class UnallowedArgumentMessage(Message):
    def __init__(self, option: object = "") -> None:
        if isinstance(option, UnallowedArgumentMessage):
            option = option.option
        self.option = str(option)

    def __str__(self: Self, /) -> str:
        return "option '%s' doesn't allow an argument" % self.option

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, UnallowedArgumentMessage)
            and self.option == other.option
        )

    def __repr__(self) -> str:
        return f"UnallowedArgumentMessage({self.option!r})"

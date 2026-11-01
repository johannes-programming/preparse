from typing import Self

from preparse.abc.Message import Message


class AmbiguousOptionMessage(Message):
    def __init__(
        self, option: object = "", possibilities: object = ()
    ) -> None:
        if isinstance(option, AmbiguousOptionMessage):
            other = option
            option, possibilities = other.option, other.possibilities
        self.option = str(option)
        self.possibilities = list(possibilities)

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

    def __repr__(self) -> str:
        return (
            f"AmbiguousOptionMessage({self.option!r}, {self.possibilities!r})"
        )

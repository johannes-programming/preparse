__all__: list[str] = ["Bundle"]

from typing import Any, Self

from preparse._items.Option import Option


class Bundle(Option):

    __slots__ = (
        "_chars",
        "_joined",
        "_argmode",
        "_right",
    )

    def __init__(
        self: Self,
        /,
        *,
        argmode: str,
        chars: str,
        joined: bool = False,
        right: str | None = None,
    ) -> None:
        self.chars = chars
        self.joined = joined
        self.argmode = argmode
        self.right = right

    @staticmethod
    def _split_long_enabled(chars: str) -> list[str]:
        ans: list[str]
        x: str
        ans = list()
        for x in chars:
            if x == "-":
                ans[-1] += "-"
            else:
                ans.append(x)
        return ans

    @staticmethod
    def _split_shortonly(chars: str) -> list[str]:
        ans: list[str]
        x: str
        ans = list()
        x = chars
        while x:
            if x == "-":
                if ans:
                    ans[0] = "-" + ans[0]
                else:
                    ans.append("-")
                x = ""
            elif x.endswith("-"):
                ans.insert(0, x[-2:])
                x = x[:-2]
            else:
                ans.insert(0, x[-1])
                x = x[:-1]
        return ans

    @property
    def chars(self: Self, /) -> str:
        return self._chars

    @chars.setter
    def chars(self: Self, x: object, /) -> None:
        self._chars = str(x)

    def deparse(self: Self, /) -> list[str]:
        if self.right is None:
            return ["-" + self.chars]
        elif self.joined:
            return ["-" + self.chars + self.right]
        else:
            return ["-" + self.chars, self.right]

    def split(self: Self, /, *, long_enabled: bool) -> list[Self]:
        ans: list[Self]
        parts: list[str]
        x: str
        if long_enabled:
            parts = self._split_long_enabled(self.chars)
        else:
            parts = self._split_shortonly(self.chars)
        ans = list()
        for x in parts:
            ans.append(type(self)(chars=x, argmode=""))
        self.chars = ans[-1].chars
        ans[-1] = self
        return ans

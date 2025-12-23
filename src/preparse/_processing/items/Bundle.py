from typing import *

import setdoc

from preparse._processing.items.Item import Item
from preparse._processing.items.Option import Option
from preparse._utils.dataprop import dataprop
from preparse.core.enums import *

__all__ = ["Bundle"]


class Bundle(Option):

    chars: str
    joined: bool
    nargs: Nargs
    right: Optional[str]

    __slots__ = ()

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        chars: str,
        joined: bool = False,
        right: Optional[str] = None,
    ) -> None:
        self.chars = chars
        self.joined = joined
        self.right = right

    @classmethod
    def _split_allowslong(cls: type, chars: str) -> list[str]:
        ans: list[str]
        x: str
        ans = list()
        for x in chars:
            if x == "-":
                ans[-1].chars += "-"
            else:
                ans.append(x)
        return ans

    @classmethod
    def _split_shortonly(cls: type, chars: str) -> list[str]:
        ans: list[str]
        x: str
        ans = list()
        x = chars
        while x:
            if x == "-":
                ans[0] = "-" + ans[0]
                x = ""
            elif x.endswith("-"):
                ans.insert(0, x[-2:])
                x = x[:-2]
            else:
                ans.insert(0, x[-1])
                x = x[:-1]
        return ans

    @dataprop
    def chars(self: Self, x: Any) -> str:
        return str(x)

    def deparse(self: Self) -> list[str]:
        if self.right is None:
            return ["-" + self.chars]
        elif self.joined:
            return ["-" + self.chars + self.right]
        else:
            return ["-" + self.chars, self.right]

    def split(self: Self, *, allowslong: bool) -> list[Item]:
        ans: list[Self]
        parts: list[str]
        x: str
        if allowslong:
            parts = self._split_allowslong(self.chars)
        else:
            parts = self._split_shortonly(self.chars)
        ans = list()
        for x in parts:
            ans.append(Bundle(chars=x))
        self.chars = ans[-1].chars
        ans[-1] = self
        return ans

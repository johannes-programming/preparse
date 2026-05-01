from typing import *

import setdoc

from preparse._utils import *
from preparse.warners.Warner import Warner

__all__ = ["DualWarner"]


class DualWarner(Warner):
    __slots__ = ()
    option: str
    prog: str

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any, islong: Any) -> None:
        self.prog = prog
        self.option = option
        self.islong = islong

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        if self.islong:
            return type(self)._longmsg % self.option
        else:
            return type(self)._shortmsg % self.option

    @dataprop
    def islong(self: Self, value: Any) -> bool:
        return bool(value)

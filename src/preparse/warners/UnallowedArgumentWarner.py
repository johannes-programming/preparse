from typing import *

import setdoc

from preparse._utils import *
from preparse.warners.LongonlyWarner import LongonlyWarner

__all__ = ["UnallowedArgumentWarner"]


class UnallowedArgumentWarner(LongonlyWarner):

    __slots__ = ()
    option: str
    prog: str
    # option is always full key without value

    @setdoc.basic
    def __init__(self: Self, *, prog: Any, option: Any) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

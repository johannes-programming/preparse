__all__: list[str] = ["UnallowedArgumentMessage"]

from typing import Self

import setdoc

from preparse.abc.LongonlyMessage import LongonlyMessage


class UnallowedArgumentMessage(LongonlyMessage):

    # option is always full key without value

    @setdoc.basic
    def __post_init__(self: Self, *, option: object, prog: object) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

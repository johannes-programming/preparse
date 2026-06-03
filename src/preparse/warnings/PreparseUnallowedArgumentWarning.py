from typing import Any, Self

import setdoc

from preparse.warnings.PreparseLongonlyWarning import PreparseLongonlyWarning

__all__ = ["PreparseUnallowedArgumentWarning"]


class PreparseUnallowedArgumentWarning(PreparseLongonlyWarning):

    # option is always full key without value

    @setdoc.basic
    def __post_init__(self: Self, *, prog: Any, option: Any) -> None:
        self.prog = prog
        self.option = option

    def getmsg(self: Self) -> str:
        "This method returns the core message."
        return "option '%s' doesn't allow an argument" % self.option

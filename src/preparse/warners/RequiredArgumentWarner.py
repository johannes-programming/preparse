from typing import *

from preparse.warners.DualWarner import DualWarner

__all__ = ["RequiredArgumentWarner"]


class RequiredArgumentWarner(DualWarner):
    __slots__ = ()
    args: tuple[str]
    option: str
    prog: str
    _longmsg = "option '%s' requires an argument"
    _shortmsg = "option requires an argument -- '%s'"

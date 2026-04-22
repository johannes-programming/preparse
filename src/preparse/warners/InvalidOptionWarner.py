from typing import *

from preparse.warners.DualWarner import DualWarner

__all__ = ["InvalidOptionWarner"]


class InvalidOptionWarner(DualWarner):
    __slots__ = ()
    args: tuple[str]
    option: str
    prog: str
    _longmsg = "unrecognized option '%s'"
    _shortmsg = "invalid option -- '%s'"

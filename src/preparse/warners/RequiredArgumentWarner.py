from typing import *

from preparse._utils import *
from preparse.warners.DualWarner import DualWarner

__all__ = ["RequiredArgumentWarner"]


class RequiredArgumentWarner(DualWarner):
    __slots__ = ()
    option: str
    prog: str
    _longmsg = "option '%s' requires an argument"
    _shortmsg = "option requires an argument -- '%s'"

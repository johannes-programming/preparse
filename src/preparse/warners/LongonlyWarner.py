from typing import *

from preparse._utils import *
from preparse.warners.Warner import Warner

__all__ = ["LongonlyWarner"]


class LongonlyWarner(Warner):
    __slots__ = ()
    option: str
    prog: str
    # only possible for long options

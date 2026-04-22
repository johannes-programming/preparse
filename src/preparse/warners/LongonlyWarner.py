from typing import *

from preparse.warners.WarnerABC import WarnerABC

__all__ = ["LongonlyWarner"]


class LongonlyWarner(WarnerABC):
    __slots__ = ()
    args: tuple[str]
    option: str
    prog: str
    # only possible for long options

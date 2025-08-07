import dataclasses
import functools
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Item"]


@dataclasses.dataclass
class Item:
    full: Optional[str] = None
    joined: bool = False
    left: Optional[str] = None
    nargs: Optional[Nargs] = None
    right: Optional[str] = None

    def ishungry(self: Self) -> bool:
        return self.right is None and self.nargs == Nargs.REQUIRED_ARGUMENT

    def isoption(self: Self) -> bool:
        return self.left is not None

    def islong(self: Self) -> bool:
        return self.isoption() and self.left.startswith("-")

    def isgroup(self: Self) -> bool:
        return self.isoption() and not self.left.startswith("-")

    def isspecial(self: Self) -> bool:
        return self.left is None and self.right is None

    def ispositional(self: Self) -> bool:
        return self.left is None and self.right is not None

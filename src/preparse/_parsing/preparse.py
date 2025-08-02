import dataclasses
import functools
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *
from preparse._parsing.parse import *
from preparse._parsing.deparse import *
from preparse._parsing.digest import *
from preparse._parsing.Item import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["preparse"]

def preparse(parser: "PreParser", args: list[str]) -> list[str]:
    olditems:list[Item] = list(parse(args, parser=parser))
    newitems:list[Item] = list(digest(olditems, parser=parser))
    ans:list[str] = list(deparse(newitems, parser=parser))
    return ans

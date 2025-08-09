import sys
from typing import *

from preparse._parsing.deparse import *
from preparse._parsing.digest import *
from preparse._parsing.Item import *
from preparse._parsing.parse import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["process"]


def process(
    *,
    args: Optional[Iterable] = None,
    parser: "PreParser",
) -> list[str]:
    "This method parses args."
    items: list[Item] = parse(
        args, 
        cause_warning=parser.cause_warning,
        islongonly=parser.islongonly,
        optdict=parser.optdict,
    )
    items: list[Item] = list(digest(items, parser=parser))
    ans: list[str] = list(deparse(items))
    return ans

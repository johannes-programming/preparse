import sys
from typing import *

from preparse._parsing.deparse import *
from preparse._parsing.digest import *
from preparse._parsing.Item import *
from preparse._parsing.parse import *
from preparse.core.enums import *
from preparse.core.PreParser import *
import types



__all__ = ["process"]


def process(args: Optional[Iterable] = None,*,parser:"PreParser") -> list[str]:
    "This method parses args."
    items: list[Item] = parse(
        args,
        cause_warning=parser.cause_warning,
        islongonly=parser.islongonly, 
        isposix=parser.order==Order.POSIX, 
        optdict=parser.optdict, 
        rejectabbr=parser.abbr==Abbr.REJECT, 
    )
    items: list[Item] = digest(
        list(items), 
        parser=parser,
    )
    ans: list[str] = list(deparse(items=items))
    return ans

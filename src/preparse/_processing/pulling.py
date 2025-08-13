import sys
from typing import *

from preparse._processing.items import *

__all__ = ["pull"]


def pull(args: Optional[Iterable]) -> list[Item]:
    argiter: Iterable = sys.argv[1:] if args is None else args
    x: Any
    ans: list[Item] = list()
    for x in argiter:
        ans.append(Positional(x))
    return ans

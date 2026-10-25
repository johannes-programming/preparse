__all__: list[str] = ["pull"]

import sys
from typing import *

from preparse._items.Positional import Positional


def pull(args: Optional[Iterable] = None) -> list[Positional]:
    "This method acquires args."
    argiter: Iterable
    if args is None:
        argiter = sys.argv[1:]
    else:
        argiter = args
    return list(map(Positional, argiter))

import sys
from collections.abc import Iterable
from typing import Optional

from preparse._items.Item import Item
from preparse._items.Positional import Positional

__all__ = ["pull"]


def pull(args: Optional[Iterable[object]] = None) -> list[Item]:
    "This method acquires args."
    argiter: Iterable[object]
    if args is None:
        argiter = sys.argv[1:]
    else:
        argiter = args
    return list(map(Positional, argiter))

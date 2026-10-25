__all__: list[str] = ["pull"]

import sys
from collections.abc import Iterable
from typing import Any

from preparse._items.Positional import Positional


def pull(args: Iterable[Any] | None = None) -> list[Positional]:
    "This method acquires args."
    argiter: Iterable[Any]
    if args is None:
        argiter = sys.argv[1:]
    else:
        argiter = args
    return list(map(Positional, argiter))

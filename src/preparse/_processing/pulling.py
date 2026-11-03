__all__: list[str] = ["pull"]

import sys
from collections.abc import Iterable

from preparse._items.Item import Item
from preparse._items.Positional import Positional
from preparse.enum.Infer import Infer


def pull(args: Iterable[object] | Infer = Infer.INFER) -> list[Item]:
    "This method acquires args."
    argiter: Iterable[object]
    if isinstance(args, Infer):
        argiter = sys.argv[1:]
    else:
        argiter = args
    return list(map(Positional, argiter))

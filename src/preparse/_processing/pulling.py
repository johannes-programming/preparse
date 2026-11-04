__all__: list[str] = ["pull"]

import sys
from collections.abc import Iterable

from preparse.enum.Infer import Infer


def pull(args: Iterable[object] | Infer = Infer.INFER) -> list[str]:
    "This method acquires args."
    argiter: Iterable[object]
    if isinstance(args, Infer):
        argiter = sys.argv[1:]
    else:
        argiter = args
    return list(map(str, argiter))

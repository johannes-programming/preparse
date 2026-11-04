__all__: list[str] = ["process"]

from collections.abc import Iterable

from preparse._items.Item import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.abc.Message import Message
from preparse.enum.Infer import Infer
from preparse.enum.Tuning import Tuning


def process(
    args: Iterable[object] | Infer = Infer.INFER,
    *,
    abbr: Tuning,
    bundling: Tuning,
    reverse: tuple[bool, str] | None,
    is_posix: bool,
    joined: Tuning,
    longopts: tuple[str, ...] | None,
    reconcilesorders: bool,
    shortopts: str | None,
    special: Tuning,
) -> tuple[list[str], list[Message]]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items, messages = parse(
        items,
        shortopts=shortopts,
        longopts=longopts,
        is_posix=is_posix,
        reverse=reverse,
    )
    items = digest(
        items,
        long_enabled=longopts is not None,
        short_enabled=shortopts is not None,
        bundling=bundling,
        abbr=abbr,
        joined=joined,
        longopts=longopts,
        is_posix=is_posix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    preparsed = deparse(items)
    return preparsed, messages

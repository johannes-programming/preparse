__all__: list[str] = ["process"]

from collections.abc import Iterable
from typing import Optional

from preparse._items.Item import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.abc.Message import Message
from preparse.enum.Tuning import Tuning


def process(
    args: Optional[Iterable[object]] = None,
    *,
    shortopts: str | None,
    longopts: tuple[str, ...] | None,
    bundling: Tuning,
    expandsabbr: bool,
    expectsposix: bool,
    prog: str,
    reconcilesorders: bool,
    special: Tuning,
) -> tuple[list[str], list[Message]]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items, messages = parse(
        items,
        shortopts=shortopts,
        longopts=longopts,
        expectsposix=expectsposix,
        prog=prog,
    )
    items = digest(
        items,
        long_enabled=longopts is not None,
        short_enabled=shortopts is not None,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    preparsed = deparse(items)
    return preparsed, messages

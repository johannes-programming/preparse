__all__: list[str] = ["process"]

from collections.abc import Iterable
from typing import Any, Optional

from preparse._items.Item import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.abc.Message import Message
from preparse.enums.Tuning import Tuning


def process(
    args: Optional[Iterable[object]] = None,
    *,
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsposix: bool,
    optdict: dict[Any, Any],
    prog: str,
    reconcilesorders: bool,
    special: Tuning,
) -> tuple[list[str], list[Message]]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items, messages = parse(
        items,
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=optdict,
        prog=prog,
    )
    items = digest(
        items,
        allowslong=allowslong,
        allowsshort=allowsshort,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    preparsed = deparse(items)
    return preparsed, messages

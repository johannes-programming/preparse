__all__: list[str] = ["process"]

from collections.abc import Iterable
from typing import Any, Optional

from preparse._items.Item import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse._option_spec import option_modes
from preparse.abc.Message import Message
from preparse.enum.Tuning import Tuning


def process(
    args: Optional[Iterable[object]] = None,
    *,
    shortsopts: str | None,
    longopts: tuple[str, ...] | None,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsposix: bool,
    prog: str,
    reconcilesorders: bool,
    special: Tuning,
) -> tuple[list[str], list[Message]]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    has_longopts = longopts is not None
    has_shortopts = shortsopts is not None
    modes = option_modes(shortsopts, longopts)
    items, messages = parse(
        items,
        has_longopts=has_longopts,
        has_shortopts=has_shortopts,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        modes=modes,
        prog=prog,
    )
    items = digest(
        items,
        has_longopts=has_longopts,
        has_shortopts=has_shortopts,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    preparsed = deparse(items)
    return preparsed, messages

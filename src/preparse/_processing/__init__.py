__all__: list[str] = ["process"]

from types import FunctionType
from typing import Iterable

from preparse._items import Bundle, Item, Long, Option, Positional, Special
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse._utils import dataprop
from preparse.core.enums import Nargs, Tuning


def process(
    args: Iterable | None = None,
    *,
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsposix: bool,
    optdict: dict,
    prog: str,
    reconcilesorders: bool,
    special: Tuning,
    warn: FunctionType,
) -> list[str]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items = parse(
        items,
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=optdict,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowslong=allowslong,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    return deparse(items)

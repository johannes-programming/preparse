from types import FunctionType
from typing import *

import datahold

from preparse._items import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.enums.Tuning import Tuning

__all__ = ["process"]


def process(
    args: Optional[Iterable] = None,
    *,
    abbr: Optional[Tuning],
    allowsLong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expectsPOSIX: bool,
    optNaming: datahold.DataNaming,
    prog: str,
    reconcilesOrders: bool,
    special: Tuning,
    warn: FunctionType,
) -> list[str]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items = parse(
        items,
        abbr=abbr,
        allowsLong=allowsLong,
        allowsshort=allowsshort,
        expectsPOSIX=expectsPOSIX,
        optNaming=optNaming,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowsLong=allowsLong,
        bundling=bundling,
        expectsPOSIX=expectsPOSIX,
        reconcilesOrders=reconcilesOrders,
        special=special,
    )
    return deparse(items)

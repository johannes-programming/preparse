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
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expectsPOSIX: bool,
    optNaming: datahold.DataNaming,
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
        abbr=abbr,
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsPOSIX=expectsPOSIX,
        optNaming=optNaming,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowslong=allowslong,
        bundling=bundling,
        expectsPOSIX=expectsPOSIX,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    return deparse(items)

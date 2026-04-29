from types import FunctionType
from typing import *

from preparse._items import *
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse._utils import *
from preparse.core.enums import *
from datahold import HoldNaming

__all__ = ["process"]


def process(
    args: Optional[Iterable] = None,
    *,
    abbr: Optional[Tuning],
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expectsposix: bool,
    optNaming: HoldNaming,
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
        expectsposix=expectsposix,
        optNaming=optNaming,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowslong=allowslong,
        bundling=bundling,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    return deparse(items)

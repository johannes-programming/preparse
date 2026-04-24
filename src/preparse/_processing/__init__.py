from types import FunctionType
from typing import *

from preparse._items import *
from preparse._processing.deparsing import *
from preparse._processing.digesting import *
from preparse._processing.parsing import *
from preparse._processing.pulling import *
from preparse._utils import *
from preparse.enums import *

__all__ = ["process"]


def process(
    args: Optional[Iterable] = None,
    *,
    allowsLong: bool,
    allowsShort: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsPOSIX: bool,
    optDict: dict,
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
        allowsLong=allowsLong,
        allowsShort=allowsShort,
        expectsabbr=expectsabbr,
        expectsPOSIX=expectsPOSIX,
        optDict=optDict,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowsLong=allowsLong,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsPOSIX=expectsPOSIX,
        reconcilesOrders=reconcilesOrders,
        special=special,
    )
    return deparse(items)

from types import FunctionType
from typing import *

from preparse._items import *
from preparse._processing.deparsing import *
from preparse._processing.digesting import *
from preparse._processing.parsing import *
from preparse._processing.pulling import *
from preparse._utils import *
from preparse.core.enums import *

__all__ = ["process"]


def process(
    args: Optional[Iterable] = None,
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
    abbr: Optional[Tuning]
    items: list[Item]
    if not expectsabbr:
        abbr = None
    elif expandsabbr:
        abbr = Tuning.MINIMIZE
    else:
        abbr = Tuning.MAINTAIN
    items = pull(args)
    items = parse(
        items,
        abbr=abbr,
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsposix=expectsposix,
        optdict=optdict,
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

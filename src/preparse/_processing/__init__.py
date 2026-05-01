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
    abbr: Optional[Tuning],
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expectsposix: bool,
    optNaming: dict,
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

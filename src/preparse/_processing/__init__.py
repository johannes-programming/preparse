from types import FunctionType
from typing import *

from preparse._processing.deparsing import *
from preparse._processing.digesting import *
from preparse._processing.items import *
from preparse._processing.parsing import *
from preparse._processing.pulling import *
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
    items: list[str] = pull(args)
    items: list[Item] = parse(
        items,
        optdict=optdict,
        expectsabbr=expectsabbr,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        prog=prog,
        warn=warn,
        allowslong=allowslong,
        allowsshort=allowsshort,
    )
    items: list[Item] = digest(
        items,
        special=special,
        reconcilesorders=reconcilesorders,
        expectsposix=expectsposix,
        bundling=bundling,
    )
    ans: list[str] = deparse(items)
    return ans

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
        allowslong=allowslong,
        allowsshort=allowsshort,
        expandsabbr=expandsabbr,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=optdict,
        prog=prog,
        warn=warn,
    )
    items: list[Item] = digest(
        items,
        bundling=bundling,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    ans: list[str] = deparse(items)
    return ans

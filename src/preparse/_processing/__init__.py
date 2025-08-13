from typing import *

from preparse._processing.deparsing import *
from preparse._processing.digesting import *
from preparse._processing.items import *
from preparse._processing.parsing import *
from preparse._processing.pulling import *

if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser

__all__ = ["process"]


def process(
    args: Optional[Iterable] = None,
    *,
    parser: "PreParser",
) -> list[str]:
    "This method parses args."
    parser = parser.copy()
    items: list[str] = pull(args)
    items: list[Item] = parse(
        items,
        optdict=parser.optdict,
        expectsabbr=parser.expectsabbr,
        expandsabbr=parser.expandsabbr,
        expectsposix=parser.expectsposix,
        prog=parser.prog,
        warn=parser.warn,
        allowslong=parser.allowslong,
        allowsshort=parser.allowsshort,
    )
    items: list[Item] = digest(
        items,
        special=parser.special,
        reconcilesorders=parser.reconcilesorders,
        expectsposix=parser.expectsposix,
        bundling=parser.bundling,
    )
    ans: list[str] = deparse(items)
    return ans

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
    *,
    args: Optional[Iterable] = None,
    parser: "PreParser",
) -> list[str]:
    "This method parses args."
    parser = parser.copy()
    items:list[str] = list(pull(args))
    items: list[Item] = list(parse(items, parser=parser))
    items: list[Item] = list(digest(items, parser=parser))
    ans: list[str] = list(deparse(items))
    return ans

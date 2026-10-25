__all__: list[str] = ["process"]

from collections.abc import Iterable
from types import FunctionType
from typing import Any

from preparse._items import Item, Positional
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.core.enums import Nargs, Tuning


def process(
    args: Iterable[Any] | None = None,
    *,
    allowslong: bool,
    allowsshort: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsposix: bool,
    optdict: dict[str, Nargs],
    prog: str,
    reconcilesorders: bool,
    special: Tuning,
    warn: FunctionType,
) -> list[str]:
    "This method parses args."
    items: list[Item]
    positionals: list[Positional]
    positionals = pull(args)
    items = parse(
        positionals,
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=optdict,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items,
        allowslong=allowslong,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    return deparse(items)

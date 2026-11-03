__all__: list[str] = ["process"]

from collections.abc import Iterable
from typing import Optional

from preparse._items.Item import Item
from preparse._processing.deparsing import deparse
from preparse._processing.digesting import digest
from preparse._processing.parsing import parse
from preparse._processing.pulling import pull
from preparse.abc.Message import Message
from preparse.enum.Nargs import Nargs
from preparse.enum.Tuning import Tuning


def process(
    args: Optional[Iterable[object]] = None,
    *,
    bundling: Tuning,
    expandsabbr: bool,
    expectsabbr: bool,
    expectsposix: bool,
    longopts: tuple[str, ...] | None,
    prog: str,
    reconcilesorders: bool,
    shortopts: str | None,
    special: Tuning,
) -> tuple[list[str], list[Message]]:
    "This method parses args."
    items: list[Item]
    items = pull(args)
    items, messages = parse(
        items,
        allowslong=longopts is not None,
        allowsshort=shortopts is not None,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=_optdict(longopts=longopts, shortopts=shortopts),
        prog=prog,
    )
    items = digest(
        items,
        allowslong=longopts is not None,
        allowsshort=shortopts is not None,
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    preparsed = deparse(items)
    return preparsed, messages


def _optdict(
    *, longopts: tuple[str, ...] | None, shortopts: str | None
) -> dict[str, Nargs]:
    ans = dict()
    if longopts is not None:
        for x in reversed(longopts):
            if x.endswith("=?"):
                n = Nargs.OPTIONAL_ARGUMENT
                y = x[:-2]
            elif x.endswith("="):
                n = Nargs.REQUIRED_ARGUMENT
                y = x[:-1]
            else:
                n = Nargs.NO_ARGUMENT
                y = x
            if shortopts is None:
                y = "-" + y
            else:
                y = "--" + y
            ans[y] = n
    if shortopts is not None:
        m = 0
        for x in reversed(shortopts):
            if x == ":":
                m += 1
                continue
            ans["-" + x] = Nargs(m)
            m = 0
    return dict(reversed(ans.items()))

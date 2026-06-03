from collections.abc import Hashable, Iterable
from typing import Any, Optional, Self, cast

import cmp3
import datahold
import setdoc
from frozendict import frozendict

from preparse.enums.Nargs import Nargs
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem

__all__ = ["Optdict"]


def nargs(value: Any, /) -> Nargs:
    if isinstance(value, int):
        return Nargs(value)
    else:
        return Nargs.OPTIONAL_ARGUMENT


class Optdict(
    cmp3.CmpABC,
    datahold.HoldDict[str, Nargs],
):
    __slots__ = ()

    _data: frozendict[str, Nargs]

    @setdoc.basic
    def __cmp__(self: Self, other: Any, /) -> Optional[int]:
        if type(self) is type(other):
            return cast(
                Optional[int],
                cmp3.cmp(self._data, other._data, mode="eq_strict"),
            )
        else:
            return cast(
                Optional[int], cmp3.cmp(self._data, other, mode="eq_strict")
            )

    __init__ = datahold.HoldDict[Hashable, object].__init__

    @property
    def data(self: Self) -> frozendict[str, Nargs]:
        return frozendict(self._data)

    @data.setter  # type: ignore[override]
    def data(
        self: Self,
        value: SupportsKeysAndGetitem | Iterable[tuple[Hashable, object]],
        /,
    ) -> None:
        a: frozendict[Hashable, object]
        b: list[tuple[str, Nargs]]
        x: Hashable
        y: object
        a = frozendict(value)  # type: ignore[arg-type]
        b = list()
        for x, y in a.items():
            if isinstance(y, int):
                b.append((str(x), Nargs(y)))
            else:
                b.append((str(x), Nargs.OPTIONAL_ARGUMENT))
        b.sort()
        self._data = frozendict(b)

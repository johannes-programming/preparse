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


class Optdict(cmp3.CmpABC, datahold.HoldDict[str, Nargs]):
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

    @property  # type: ignore[override]
    def data(self: Self) -> frozendict[str, Nargs]:
        return frozendict(self._data)

    @data.setter
    def data(
        self: Self,
        value: SupportsKeysAndGetitem | Iterable[tuple[Hashable, object]],
        /,
    ) -> None:
        a: frozendict[Hashable, object]
        x: map[str]
        y: map[Nargs]
        a = frozendict(value)
        x = map(str, a.keys())
        y = map(nargs, a.values())
        self._data = frozendict(zip(x, y, strict=True))

__all__: list[str] = ["Optdict"]

from collections.abc import Hashable, Iterable
from typing import Any, Optional, Self, TypeVar, cast

import cmp3
import datahold
import setdoc
from frozendict import frozendict

from preparse.enum.Nargs import Nargs
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem

Key = TypeVar("Key", bound=Hashable)


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

    def __init__(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key, int | None]
            | Iterable[tuple[Key, int | None]]
        ) = (),
        /,
        **kwargs: int | None,
    ) -> None:
        self._data = frozendict()
        self.update(other, **kwargs)

    def __or__(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key, int | None]
            | Iterable[tuple[Key, int | None]]
        ),
        /,
    ) -> Self:
        return type(self)(
            self.data | frozendict(other)  # type: ignore[arg-type]
        )

    @property
    def data(self: Self, /) -> frozendict[str, Nargs]:
        return frozendict(self._data)

    @data.setter
    def data(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key, int | None]
            | Iterable[tuple[Key, int | None]]
        ),
        /,
    ) -> None:
        a: frozendict[Key, int | None]
        b: list[tuple[str, Nargs]]
        x: Key
        y: int | None
        a = frozendict(other)  # type: ignore[arg-type]
        b = list()
        for x, y in a.items():
            if isinstance(y, int):
                b.append((str(x), Nargs(y)))
            else:
                b.append((str(x), Nargs.OPTIONAL_ARGUMENT))
        b.sort()
        self._data = frozendict(b)

    def update(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key, int | None]
            | Iterable[tuple[Key, int | None]]
        ) = (),
        /,
        **kwargs: int | None,
    ) -> None:
        self.data = self.data | frozendict(other) | kwargs  # type: ignore[arg-type]

from __future__ import annotations

__all__: list[str] = ["SupportsKeysAndGetitem"]

from collections.abc import Iterable
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class SupportsKeysAndGetitem[Key, Value](Protocol):
    def __getitem__(self: Self, key: Key, /) -> Value: ...
    def keys(self: Self, /) -> Iterable[Key]: ...

__all__: list[str] = ["SupportsKeysAndGetitem"]

from collections.abc import Hashable
from typing import Protocol, Self


class SupportsKeysAndGetitem(Protocol):
    def __getitem__(self: Self, key: Hashable, /) -> object: ...
    def keys(self: Self) -> tuple[Hashable, ...]: ...

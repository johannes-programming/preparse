from collections.abc import Hashable
from typing import Protocol, Self

__all__ = ["SupportsKeysAndGetitem"]


class SupportsKeysAndGetitem(Protocol):
    def __getitem__(self: Self, key: Hashable, /) -> object: ...
    def keys(self: Self) -> tuple[Hashable, ...]: ...

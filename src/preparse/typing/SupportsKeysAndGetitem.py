__all__: list[str] = ["SupportsKeysAndGetitem"]

from collections.abc import Hashable, Iterable
from typing import Protocol, Self

from typing_extensions import TypeVar

Key = TypeVar("Key", bound=Hashable, default=Hashable)
Value = TypeVar("Value", covariant=True, default=int | None)


class SupportsKeysAndGetitem(Protocol[Key, Value]):
    def __getitem__(self: Self, key: Key, /) -> Value: ...
    def keys(self: Self, /) -> Iterable[Key]: ...

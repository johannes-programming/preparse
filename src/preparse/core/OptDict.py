from __future__ import annotations

__all__: list[str] = ["OptDict"]

from collections.abc import Iterable
from typing import (
    Any,
    Final,
    Protocol,
    Self,
    TypeVar,
    overload,
    runtime_checkable,
)

from preparse.enum.Nargs import Nargs

Key = TypeVar("Key")
Value = TypeVar("Value")


@runtime_checkable
class SupportsKeysAndGetitem(Protocol[Key]):
    def __getitem__(self: Self, key: Key, /) -> object: ...
    def keys(self: Self, /) -> Iterable[Key]: ...


class OptDict(dict[str, Nargs]):
    """A dictionary which normalizes keys and argument-count values."""

    Nargs: Final[type[Nargs]] = Nargs

    def __contains__(self: Self, key: object, /) -> bool:
        return dict.__contains__(self, str(key))

    def __delitem__(self: Self, key: object, /) -> None:
        dict.__delitem__(self, str(key))

    def __getitem__(self: Self, key: object, /) -> Nargs:
        return dict.__getitem__(self, str(key))

    def __init__(
        self: Self,
        other: (
            SupportsKeysAndGetitem | Iterable[tuple[object, object]] | None
        ) = None,
        /,
        **kwargs: object,
    ) -> None:
        super().__init__()
        self.update(other, **kwargs)

    def __ior__(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key]
            | Iterable[tuple[object, object]]
            | None
        ),
        /,
    ) -> OptDict:
        self.update(other)
        return self

    def __or__(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key]
            | Iterable[tuple[object, object]]
            | None
        ),
        /,
    ) -> OptDict:
        result = self.copy()
        result.update(other)
        return result

    def __repr__(self: Self, /) -> str:
        return f"{type(self).__name__}({dict(self)})"

    def __setitem__(self: Self, key: object, value: object, /) -> None:
        if value is None:
            return
        dict.__setitem__(self, str(key), self.Nargs(value))

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @classmethod
    def fromkeys(
        cls: type[Self], /, keys: Iterable[object], value: object = None
    ) -> Self:
        ans: Self
        ans = cls()
        if value is None:
            return cls()
        for key in keys:
            ans[key] = value
        return ans

    @overload
    def get(
        self: Self, key: object, default: None = None, /
    ) -> Nargs | None: ...
    @overload
    def get(self: Self, key: object, default: Value, /) -> Nargs | Value: ...
    def get(self: Self, key: object, default: Any = None, /) -> Any:
        return dict.get(self, str(key), default)

    @overload
    def pop(self: Self, key: object, /) -> Nargs: ...
    @overload
    def pop(self: Self, key: object, default: Value, /) -> Nargs | Value: ...
    def pop(self: Self, key: object, /, *args: Any) -> Any:
        return dict.pop(self, str(key), *args)

    def setdefault(self: Self, key: object, default: object = None) -> Nargs:
        key = str(key)
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        self[key] = default
        return dict.__getitem__(self, key)

    def update(
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key]
            | Iterable[tuple[object, object]]
            | None
        ) = None,
        /,
        **kwargs: object,
    ) -> None:
        if other is not None and isinstance(other, SupportsKeysAndGetitem):
            for x in other.keys():
                self[str(x)] = OptDict.Nargs(other[x])
        elif other is not None:
            for x, y in other:
                self[str(x)] = OptDict.Nargs(y)
        for x, y in kwargs.items():
            self[str(x)] = OptDict.Nargs(y)

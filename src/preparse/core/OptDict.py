from __future__ import annotations

__all__: list[str] = ["OptDict"]

from collections.abc import Iterable
from typing import Any, Final, Self, overload

from preparse.enum.Nargs import Nargs
from preparse.typing.OptDictOther import OptDictOther
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem


class OptDict(dict[str, Nargs]):
    """A dictionary which normalizes keys and argument-count values."""

    Nargs: Final[type[Nargs]] = Nargs

    def __contains__(self: Self, key: object, /) -> bool:
        return dict.__contains__(self, str(key))

    def __delitem__(self: Self, key: object, /) -> None:
        dict.__delitem__(self, str(key))

    def __getitem__(self: Self, key: object, /) -> Nargs:
        return dict.__getitem__(self, str(key))

    def __init__[Key](
        self: Self,
        other: OptDictOther[Key] = None,
        /,
        **kwargs: object,
    ) -> None:
        super().__init__()
        self.update(other, **kwargs)

    def __ior__[Key](
        self: Self,
        other: OptDictOther[Key],
        /,
    ) -> Self:
        self.update(other)
        return self

    def __or__[Key](
        self: Self,
        other: OptDictOther[Key],
        /,
    ) -> Self:
        ans: Self
        ans = self.copy()
        ans.update(other)
        return ans

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
        cls: type[Self],
        keys: Iterable[object],
        value: object = None,
        /,
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
    def get[Value](
        self: Self, key: object, default: Value, /
    ) -> Nargs | Value: ...
    def get(self: Self, key: object, default: Any = None, /) -> Any:
        return dict.get(self, str(key), default)

    @overload
    def pop(self: Self, key: object, /) -> Nargs: ...
    @overload
    def pop[Value](
        self: Self, key: object, default: Value, /
    ) -> Nargs | Value: ...
    def pop(self: Self, key: object, /, *args: Any) -> Any:
        return dict.pop(self, str(key), *args)

    def setdefault(self: Self, key: object, default: object = None) -> Nargs:
        key = str(key)
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        self[key] = default
        return dict.__getitem__(self, key)

    def update[Key](
        self: Self,
        other: OptDictOther[Key] = None,
        /,
        **kwargs: object,
    ) -> None:
        if other is not None and isinstance(other, SupportsKeysAndGetitem):
            for x in other.keys():
                self[str(x)] = Nargs(other[x])
        elif other is not None:
            for x, y in other:
                self[str(x)] = Nargs(y)
        for x, y in kwargs.items():
            self[str(x)] = Nargs(y)

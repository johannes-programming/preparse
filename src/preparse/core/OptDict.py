from __future__ import annotations

__all__: list[str] = ["OptDict"]

from collections.abc import Iterable
from enum import IntEnum
from typing import Self


class OptDict(dict):
    """A dictionary which normalizes keys and argument-count values."""

    class Nargs(IntEnum):
        NO_ARGUMENT = 0
        REQUIRED_ARGUMENT = 1
        OPTIONAL_ARGUMENT = 2

        @classmethod
        def _missing_(cls: type[Self], value: object) -> OptDict.Nargs:
            if value is None:
                return cls.NO_ARGUMENT
            else:
                return cls.OPTIONAL_ARGUMENT

    def __init__(self: Self, *args: object, **kwargs: object) -> None:
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self: Self, key: object, value: object) -> None:
        key = str(key)
        if value is None and dict.__contains__(self, key):
            return
        dict.__setitem__(self, key, self.Nargs(value))

    def __getitem__(self: Self, key: object) -> Nargs:
        return dict.__getitem__(self, str(key))

    def __contains__(self: Self, key: object) -> bool:
        return dict.__contains__(self, str(key))

    def __delitem__(self: Self, key: object) -> None:
        dict.__delitem__(self, str(key))

    def get(self: Self, key: object, default: object = None) -> object:
        return dict.get(self, str(key), default)

    def pop(self: Self, key: object, *default: object) -> object:
        return dict.pop(self, str(key), *default)

    def setdefault(self: Self, key: object, default: object = None) -> Nargs:
        key = str(key)
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        self[key] = default
        return dict.__getitem__(self, key)

    def update(self: Self, *args: object, **kwargs: object) -> None:
        if len(args) > 1:
            raise TypeError("update expected at most 1 positional argument")
        if args:
            source = args[0]
            if source is not None:
                # Snapshot to make even self.update(self) well-defined.
                if hasattr(source, "keys"):
                    entries = [(key, source[key]) for key in source.keys()]
                else:
                    entries = list(source)
                for key, value in entries:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __ior__(self: Self, other: object) -> OptDict:
        self.update(other)
        return self

    def __or__(self: Self, other: object) -> OptDict:
        result = self.copy()
        result.update(other)
        return result

    def __repr__(self: Self, /) -> str:
        return f"{type(self).__name__}({dict(self)})"

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @classmethod
    def fromkeys(
        cls: type[Self], keys: Iterable[object], value: object = None
    ) -> Self:
        ans: Self
        ans = cls()
        if value is None:
            return cls()
        for key in keys:
            ans[key] = value
        return ans

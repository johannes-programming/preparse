"""Getopt-style option spelling and argument order configuration."""

__all__: list[str] = [
    "Framework",
]
from typing import Self

from preparse.abc.Representable import Representable


class Framework(Representable):
    __slots__ = ("_allows_long", "_allows_short", "_is_posix")

    def __init__(
        self,
        other: Self | None = None,
        /,
        *,
        allows_long: bool | None = None,
        allows_short: bool | None = None,
        is_posix: bool | None = None,
    ) -> None:
        self._allows_long = True
        self._allows_short = True
        self._is_posix = False
        if other is not None:
            self.allows_long = other.allows_long
            self.allows_short = other.allows_short
            self.is_posix = other.is_posix
        self.allows_long = allows_long
        self.allows_short = allows_short
        self.is_posix = is_posix

    def _dict(self: Self, /) -> dict[str, bool]:
        return dict(
            allows_long=self.allows_long,
            allows_short=self.allows_short,
            is_posix=self.is_posix,
        )

    @property
    def allows_long(self) -> bool:
        return self._allows_long

    @allows_long.setter
    def allows_long(self, value: object) -> None:
        if value is not None:
            self._allows_long = bool(value)

    @property
    def allows_short(self) -> bool:
        return self._allows_short

    @allows_short.setter
    def allows_short(self, value: object) -> None:
        if value is not None:
            self._allows_short = bool(value)

    @property
    def is_posix(self) -> bool:
        return self._is_posix

    @is_posix.setter
    def is_posix(self, value: object) -> None:
        if value is not None:
            self._is_posix = bool(value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Framework) and (
            self.allows_long,
            self.allows_short,
            self.is_posix,
        ) == (other.allows_long, other.allows_short, other.is_posix)

    def __repr__(self) -> str:
        return (
            f"Framework(allows_long={self.allows_long!r}, "
            f"allows_short={self.allows_short!r}, is_posix={self.is_posix!r})"
        )

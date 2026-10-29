from __future__ import annotations

__all__: list[str] = ["Framework"]

from typing import Self


class Framework:
    def __init__(
        self: Self,
        other: Framework | None = None,
        /,
        *,
        allows_long: bool | None = None,
        allows_short: bool | None = None,
        is_posix: bool | None = None,
    ) -> None:
        self.allows_long = True
        self.allows_short = True
        self.is_posix = False
        self.update(other)
        self.update_fields(
            allows_long=allows_long,
            allows_short=allows_short,
            is_posix=is_posix,
        )

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    def update(self: Self, other: Framework | None) -> None:
        if other is not None:
            self.update_fields(
                allows_long=other.allows_long,
                allows_short=other.allows_short,
                is_posix=other.is_posix,
            )

    def update_fields(
        self,
        *,
        allows_long: bool | None = None,
        allows_short: bool | None = None,
        is_posix: bool | None = None,
    ) -> None:
        if allows_long is not None:
            self.allows_long = allows_long
        if allows_short is not None:
            self.allows_short = allows_short
        if is_posix is not None:
            self.is_posix = is_posix

from __future__ import annotations

__all__: list[str] = ["Nargs"]

from enum import IntEnum
from typing import Self


class Nargs(IntEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

    @classmethod
    def _missing_(cls: type[Self], /, value: object) -> Nargs:
        if value is None:
            return cls(0)
        else:
            return cls(2)

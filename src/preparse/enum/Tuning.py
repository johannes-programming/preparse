from __future__ import annotations

__all__: list[str] = ["Tuning"]

from enum import IntEnum
from typing import Self


class Tuning(IntEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2

    @classmethod
    def _missing_(cls: type[Self], /, value: object) -> Tuning:
        if value is None:
            return cls(0)
        else:
            return cls(2)

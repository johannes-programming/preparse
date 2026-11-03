__all__: list[str] = ["Tuning"]

import enum
from typing import Self


class Tuning(enum.IntEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2

    @classmethod
    def _missing_(cls: type[Self], value: object) -> Self:
        return cls(2)

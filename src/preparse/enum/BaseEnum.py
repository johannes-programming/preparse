__all__: list[str] = ["BaseEnum"]

import enum
from typing import Self


class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls: type[Self], value: object) -> Self:
        return cls(2)

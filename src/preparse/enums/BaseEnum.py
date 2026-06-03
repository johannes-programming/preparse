import enum
from typing import Self

__all__ = ["BaseEnum"]


class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls: type[Self], value: object) -> Self:
        return cls(2)

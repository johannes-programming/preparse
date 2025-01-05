import enum
from typing import *


__all__ = [
    "LongOptionAbbreviations", 
    "Nargs", 
]

class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls, value):
        return cls(2)

class LongOptionAbbreviations(BaseEnum):
    REJECT = 0
    COMPLETE = 1
    KEEP = 2

class Nargs(BaseEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2


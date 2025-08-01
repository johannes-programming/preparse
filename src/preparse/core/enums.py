"This module holds the enums for the project. \
Following the precedent of getopt the value of two represents always an intermediary answer between the values zero, meaning no, and one, meaning yes."

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

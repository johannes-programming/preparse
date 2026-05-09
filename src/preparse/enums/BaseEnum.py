"""This module holds the enums for the project. \
Following the precedent of getopt, \
the value of two represents always an intermediary answer \
between the values zero, meaning no, and one, meaning yes."""

import enum
import operator
from typing import *

__all__ = ["BaseEnum"]


class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls: type, value: SupportsIndex) -> Self:
        operator.index(value)
        return cls(2)

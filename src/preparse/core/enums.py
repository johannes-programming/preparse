"""This module holds the enums for the project. \
Following the precedent of getopt, \
the value of two represents always an intermediary answer \
between the values zero, meaning no, and one, meaning yes."""

import enum
from typing import *

__all__ = [
    "Abbr",
    "Order",
    "Nargs",
]


class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls, value):
        return cls(2)


class Abbr(BaseEnum):
    REJECT = 0
    KEEP = 1
    COMPLETE = 2


class Order(BaseEnum):
    GIVEN = 0
    POSIX = 1
    PERMUTE = 2


class Nargs(BaseEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

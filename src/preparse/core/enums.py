"""This module holds the enums for the project. \
Following the precedent of getopt, \
the value of two represents always an intermediary answer \
between the values zero, meaning no, and one, meaning yes."""

__all__: list[str] = ["Nargs", "Tuning"]

import enum
from typing import Any, Self


class BaseEnum(enum.IntEnum):
    @classmethod
    def _missing_(cls: type[Self], value: Any) -> Self:
        return cls(2)


class Tuning(BaseEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2


class Nargs(BaseEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

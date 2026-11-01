from enum import IntEnum

from ._default import DefaultedEnumType


class Nargs(IntEnum, metaclass=DefaultedEnumType):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

    @classmethod
    def _missing_(cls, value):
        if value is None:
            return cls.NO_ARGUMENT
        return cls.OPTIONAL_ARGUMENT

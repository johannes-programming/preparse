from enum import IntEnum

from ._default import DefaultedEnumType


class Tuning(IntEnum, metaclass=DefaultedEnumType):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2

    @classmethod
    def _missing_(cls, value):
        if value is None:
            return cls.MINIMIZE
        return cls.MAINTAIN

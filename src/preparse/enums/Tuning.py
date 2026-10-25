from ..enums.BaseEnum import BaseEnum

__all__ = ["Tuning"]


class Tuning(BaseEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2

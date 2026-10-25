__all__: list[str] = ["Tuning"]

from ..enums.BaseEnum import BaseEnum


class Tuning(BaseEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    MAINTAIN = 2

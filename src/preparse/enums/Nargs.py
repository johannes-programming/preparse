__all__: list[str] = ["Nargs"]

from ..enums.BaseEnum import BaseEnum


class Nargs(BaseEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

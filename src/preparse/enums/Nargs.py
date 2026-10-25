from ..enums.BaseEnum import BaseEnum

__all__ = ["Nargs"]


class Nargs(BaseEnum):
    NO_ARGUMENT = 0
    REQUIRED_ARGUMENT = 1
    OPTIONAL_ARGUMENT = 2

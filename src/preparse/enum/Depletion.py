__all__: list[str] = ["Depletion"]

import enum


class Depletion(enum.Enum):
    DROP = "DROP"
    REINTERPRET = "REINTERPRET"

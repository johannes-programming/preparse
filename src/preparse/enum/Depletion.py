from __future__ import annotations

__all__: list[str] = ["Depletion"]

from enum import Enum


class Depletion(Enum):
    DROP_OPT = "DROP_OPT"
    DEFER = "DEFER"

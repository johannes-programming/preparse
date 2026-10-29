from __future__ import annotations

__all__: list[str] = []

from enum import Enum, IntEnum
from typing import Self


class Transformation:
    class Tuning(IntEnum):
        MINIMIZE = 0
        MAXIMIZE = 1
        MAINTAIN = 2

    class Depletion(Enum):
        DROP_OPT = "DROP_OPT"
        DEFER = "DEFER"

    def __init__(
        self: Self,
        other: Transformation | None = None,
        /,
        *,
        order_compatibility: Transformation.Tuning | None = None,
        bundling: Transformation.Tuning | None = None,
        abbr: Transformation.Tuning | None = None,
        equal: Transformation.Tuning | None = None,
        depletion: Transformation.Depletion | str | None = None,
    ) -> None:
        self.order_compatibility = self.Tuning.MAXIMIZE
        self.bundling = self.Tuning.MAINTAIN
        self.abbr = self.Tuning.MINIMIZE
        self.equal = self.Tuning.MAINTAIN
        self.depletion = self.Depletion.DROP_OPT
        self.update(other)
        self.update_fields(
            order_compatibility=order_compatibility,
            bundling=bundling,
            abbr=abbr,
            equal=equal,
            depletion=depletion,
        )

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    def update(self, other: Transformation | None) -> None:
        if other is not None:
            self.update_fields(
                order_compatibility=other.order_compatibility,
                bundling=other.bundling,
                abbr=other.abbr,
                equal=other.equal,
                depletion=other.depletion,
            )

    def update_fields(
        self,
        *,
        order_compatibility: Transformation.Tuning | None = None,
        bundling: Transformation.Tuning | None = None,
        abbr: Transformation.Tuning | None = None,
        equal: Transformation.Tuning | None = None,
        depletion: Transformation.Depletion | str | None = None,
    ) -> None:
        for field, value in (
            ("order_compatibility", order_compatibility),
            ("bundling", bundling),
            ("abbr", abbr),
            ("equal", equal),
        ):
            if value is not None:
                setattr(self, field, self.Tuning(value))
        if depletion is not None:
            if not isinstance(depletion, (self.Depletion, str)):
                raise TypeError(
                    "depletion must be a Depletion enum or a string"
                )
            self.depletion = depletion

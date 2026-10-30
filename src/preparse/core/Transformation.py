from __future__ import annotations

__all__: list[str] = ["Transformation"]

from typing import Final, Self

from preparse.enum.Depletion import Depletion
from preparse.enum.Tuning import Tuning


class Transformation:

    Tuning: Final[type[Tuning]] = Tuning

    def __init__(
        self: Self,
        other: Transformation | None = None,
        /,
        *,
        order_compatibility: Tuning | None = None,
        bundling: Tuning | None = None,
        abbr: Tuning | None = None,
        equal: Tuning | None = None,
        depletion: Depletion | str | None = None,
    ) -> None:
        self.order_compatibility = Tuning.MAXIMIZE
        self.bundling = Tuning.MAINTAIN
        self.abbr = Tuning.MINIMIZE
        self.equal = Tuning.MAINTAIN
        self.depletion = Depletion.DROP_OPT
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

    def update(self: Self, other: Transformation | None = None, /) -> None:
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
        order_compatibility: Tuning | None = None,
        bundling: Tuning | None = None,
        abbr: Tuning | None = None,
        equal: Tuning | None = None,
        depletion: Depletion | str | None = None,
    ) -> None:
        for field, value in (
            ("order_compatibility", order_compatibility),
            ("bundling", bundling),
            ("abbr", abbr),
            ("equal", equal),
        ):
            if value is not None:
                setattr(self, field, Tuning(value))
        if depletion is not None:
            if not isinstance(depletion, (Depletion, str)):
                raise TypeError(
                    "depletion must be a Depletion enum or a string"
                )
            self.depletion = depletion

"""The independent argument-rewriting goals."""

__all__: list[str] = [
    "Transformation",
]

from typing import Self

from preparse.abc.Copyable import Copyable
from preparse.enum.Depletion import Depletion
from preparse.enum.Tuning import Tuning


class Transformation(Copyable):
    Depletion = Depletion
    Tuning = Tuning

    def __init__(
        self,
        other: Self | None = None,
        /,
        *,
        abbr: object = None,
        bundling: object = None,
        depletion: Depletion | tuple[object, object] | None = None,
        reconciles_orders: object = None,
        separate: object = None,
        special: object = None,
    ) -> None:
        self._abbr = Tuning.MINIMIZE
        self._bundling = Tuning.MAINTAIN
        self._depletion: Depletion | tuple[bool, str] = Depletion.DROP_OPT
        self._reconciles_orders = True
        self._separate = Tuning.MAINTAIN
        self._special = Tuning.MAINTAIN
        if other is not None:
            self.abbr = other.abbr
            self.bundling = other.bundling
            self.depletion = other.depletion
            self.reconciles_orders = other.reconciles_orders
            self.separate = other.separate
            self.special = other.special
        self.abbr = abbr
        self.bundling = bundling
        self.depletion = depletion
        self.reconciles_orders = reconciles_orders
        self.separate = separate
        self.special = special

    @property
    def abbr(self) -> Tuning:
        return self._abbr

    @abbr.setter
    def abbr(self, value: object) -> None:
        if value is not None:
            self._abbr = Tuning(value)

    @property
    def bundling(self) -> Tuning:
        return self._bundling

    @bundling.setter
    def bundling(self, value: object) -> None:
        if value is not None:
            self._bundling = Tuning(value)

    @property
    def depletion(self) -> Depletion | tuple[bool, str]:
        return self._depletion

    @depletion.setter
    def depletion(self, value: object) -> None:
        if value is None:
            return
        if isinstance(value, Depletion):
            self._depletion = value
        else:
            separate, replacement = value
            self._depletion = (bool(separate), str(replacement))

    @property
    def reconciles_orders(self) -> bool:
        return self._reconciles_orders

    @reconciles_orders.setter
    def reconciles_orders(self, value: object) -> None:
        if value is not None:
            self._reconciles_orders = bool(value)

    @property
    def separate(self) -> Tuning:
        return self._separate

    @separate.setter
    def separate(self, value: object) -> None:
        if value is not None:
            self._separate = Tuning(value)

    @property
    def special(self) -> Tuning:
        return self._special

    @special.setter
    def special(self, value: object) -> None:
        if value is not None:
            self._special = Tuning(value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Transformation) and (
            self.abbr,
            self.bundling,
            self.depletion,
            self.reconciles_orders,
            self.separate,
            self.special,
        ) == (
            other.abbr,
            other.bundling,
            other.depletion,
            other.reconciles_orders,
            other.separate,
            other.special,
        )

    def __repr__(self) -> str:
        return (
            "Transformation("
            + ", ".join(
                f"{key}={getattr(self, key)!r}"
                for key in (
                    "abbr",
                    "bundling",
                    "depletion",
                    "reconciles_orders",
                    "separate",
                    "special",
                )
            )
            + ")"
        )

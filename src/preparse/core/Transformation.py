"""The independent argument-rewriting goals."""

__all__: list[str] = [
    "Transformation",
]

from typing import Any, Self

from preparse.abc.Copyable import Copyable
from preparse.enum.Depletion import Depletion
from preparse.enum.Tuning import Tuning


class Transformation(Copyable):
    __slots__ = (
        "_abbr",
        "_bundling",
        "_depletion",
        "_reconciles_orders",
        "_separate",
        "_special",
    )

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
        self._depletion = Depletion.DROP_OPT
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

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            abbr=self.abbr,
            bundling=self.bundling,
            depletion=self.depletion,
            reconciles_orders=self.reconciles_orders,
            separate=self.separate,
            special=self.special,
        )

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

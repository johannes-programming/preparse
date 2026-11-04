from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
from collections.abc import Iterable
from types import NotImplementedType
from typing import Any, Self

import setdoc
from datarepr import datarepr

from preparse._processing import process
from preparse.abc.Copyable import Copyable
from preparse.abc.Message import Message
from preparse.enum.Infer import Infer
from preparse.enum.NoChange import NoChange
from preparse.enum.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


class PreParser(Copyable):

    __slots__ = (
        "_abbr",
        "_bundling",
        "_is_posix",
        "_joined",
        "_longopts",
        "_reconciles_orders",
        "_reverse",
        "_shortopts",
        "_special",
    )
    _bundling: Tuning
    _abbr: Tuning
    _is_posix: bool
    _joined: Tuning
    _longopts: tuple[str, ...] | None
    _reconciles_orders: bool
    _reverse: tuple[bool, str] | None
    _shortopts: str | None
    _special: Tuning

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, PreParser):
            return self._dict() == other._dict()
        else:
            return NotImplemented

    @setdoc.basic
    def __init__(
        self: Self,
        other: PreParser | NoChange = NoChange.NO_CHANGE,
        /,
        *,
        abbr: int | NoChange = NoChange.NO_CHANGE,
        bundling: int | NoChange = NoChange.NO_CHANGE,
        is_posix: SupportsBool | Infer | NoChange = NoChange.NO_CHANGE,
        joined: int | NoChange = NoChange.NO_CHANGE,
        longopts: tuple[object, ...] | None | NoChange = NoChange.NO_CHANGE,
        reconciles_orders: SupportsBool | NoChange = NoChange.NO_CHANGE,
        reverse: (
            tuple[SupportsBool, object] | NoChange | None
        ) = NoChange.NO_CHANGE,
        shortopts: object = NoChange.NO_CHANGE,
        special: int | NoChange = NoChange.NO_CHANGE,
    ) -> None:
        self._abbr = Tuning.MINIMIZE
        self._bundling = Tuning.MAINTAIN
        self._is_posix = False
        self._joined = Tuning.MAINTAIN
        self._longopts = ()
        self._reconciles_orders = True
        self._reverse = None
        self._shortopts = ""
        self._special = Tuning.MAINTAIN
        if not isinstance(other, NoChange):
            self.abbr = other.abbr
            self.bundling = other.bundling
            self.is_posix = other.is_posix
            self.joined = other.joined
            self.longopts = other.longopts
            self.reconciles_orders = other.reconciles_orders
            self.reverse = other.reverse
            self.shortopts = other.shortopts
            self.special = other.special
        self.abbr = abbr
        self.bundling = bundling
        self.is_posix = is_posix
        self.joined = joined
        self.longopts = longopts
        self.reconciles_orders = reconciles_orders
        self.reverse = reverse
        self.shortopts = shortopts
        self.special = special

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self._dict())

    def _dict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        ans = dict()
        ans["bundling"] = self.bundling
        ans["abbr"] = self.abbr
        ans["joined"] = self.joined
        ans["is_posix"] = self.is_posix
        ans["longopts"] = self.longopts
        ans["reconciles_orders"] = self.reconciles_orders
        ans["reverse"] = self.reverse
        ans["shortopts"] = self.shortopts
        ans["special"] = self.special
        return ans

    @property
    def abbr(self: Self, /) -> Tuning:
        "This property determines how long options are abbreviated."
        return self._abbr

    @abbr.setter
    def abbr(self: Self, value: int | NoChange, /) -> None:
        if isinstance(value, NoChange):
            return
        self._abbr = Tuning(value)

    @property
    def bundling(self: Self, /) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._bundling

    @bundling.setter
    def bundling(self: Self, value: int | NoChange, /) -> None:
        "This property decides how to approach the bundling of short options."
        if isinstance(value, NoChange):
            return
        self._bundling = Tuning(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def reverse(self: Self, /) -> tuple[SupportsBool, object] | None:
        return self._reverse

    @reverse.setter
    def reverse(
        self: Self,
        value: tuple[SupportsBool, object] | NoChange | None,
        /,
    ) -> None:
        x: SupportsBool
        y: object
        if isinstance(value, NoChange):
            return
        if value is None:
            self._reverse = None
            return
        x, y = value
        self._reverse = bool(x), str(y)

    @property
    def is_posix(self: Self, /) -> bool:
        return self._is_posix

    @is_posix.setter
    def is_posix(
        self: Self, value: SupportsBool | Infer | NoChange, /
    ) -> None:
        if isinstance(value, NoChange):
            return
        if isinstance(value, Infer):
            self._is_posix = "POSIXLY_CORRECT" in os.environ
        else:
            self._is_posix = bool(value)

    @property
    def joined(self: Self, /) -> Tuning:
        "This property determines whether option values share the option token."
        return self._joined

    @joined.setter
    def joined(self: Self, value: int | NoChange, /) -> None:
        if isinstance(value, NoChange):
            return
        self._joined = Tuning(value)

    @property
    def longopts(self: Self, /) -> tuple[str, ...] | None:
        """getopt-style long options; None disables long-option parsing."""
        return self._longopts

    @longopts.setter
    def longopts(
        self: Self, value: tuple[object, ...] | None | NoChange, /
    ) -> None:
        if isinstance(value, NoChange):
            return
        if value is None:
            self._longopts = None
        else:
            self._longopts = tuple(map(str, value))

    def parse_args(
        self: Self,
        args: Iterable[object] | Infer = Infer.INFER,
    ) -> tuple[list[str], list[Message]]:
        "This method parses args."
        return process(
            args,
            **self._dict(),
        )

    @property
    def reconciles_orders(self: Self, /) -> bool:
        return self._reconciles_orders

    @reconciles_orders.setter
    def reconciles_orders(
        self: Self, value: SupportsBool | NoChange, /
    ) -> None:
        if isinstance(value, NoChange):
            return
        self._reconciles_orders = bool(value)

    @property
    def shortopts(self: Self, /) -> str | None:
        """getopt-style short options; None disables short-option parsing."""
        return self._shortopts

    @shortopts.setter
    def shortopts(self: Self, value: object, /) -> None:
        if isinstance(value, NoChange):
            return
        if value is None:
            self._shortopts = None
        else:
            self._shortopts = str(value)

    @property
    def special(self: Self, /) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return self._special

    @special.setter
    def special(self: Self, value: int | NoChange, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        if isinstance(value, NoChange):
            return
        self._special = Tuning(value)

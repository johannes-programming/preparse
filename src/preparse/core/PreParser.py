from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
from collections.abc import Iterable
from types import NotImplementedType
from typing import Any, Optional, Self

import setdoc
from datarepr import datarepr

from preparse._processing import process
from preparse.abc.Copyable import Copyable
from preparse.abc.Message import Message
from preparse.enum.Infer import Infer
from preparse.enum.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


class PreParser(Copyable):

    __slots__ = (
        "_bundling",
        "_expandsabbr",
        "_is_posix",
        "_longopts",
        "_reconcilesorders",
        "_shortopts",
        "_special",
    )
    _bundling: Tuning
    _expandsabbr: bool
    _is_posix: bool
    _longopts: tuple[str, ...] | None
    _reconcilesorders: bool
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
        other: PreParser | NotImplementedType = NotImplemented,
        /,
        *,
        bundling: int | NotImplementedType = NotImplemented,
        expandsabbr: SupportsBool | NotImplementedType = NotImplemented,
        is_posix: SupportsBool | Infer | NotImplementedType = NotImplemented,
        longopts: (
            tuple[object, ...] | None | NotImplementedType
        ) = NotImplemented,
        reconcilesorders: SupportsBool | NotImplementedType = NotImplemented,
        shortopts: object = NotImplemented,
        special: int | NotImplementedType = NotImplemented,
    ) -> None:
        self._bundling = Tuning.MAINTAIN
        self._expandsabbr = True
        self._is_posix = False
        self._longopts = ()
        self._reconcilesorders = True
        self._shortopts = ""
        self._special = Tuning.MAINTAIN
        if not isinstance(other, NotImplementedType):
            self.bundling = other.bundling
            self.expandsabbr = other.expandsabbr
            self.is_posix = other.is_posix
            self.longopts = other.longopts
            self.reconcilesorders = other.reconcilesorders
            self.shortopts = other.shortopts
            self.special = other.special
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.is_posix = is_posix
        self.longopts = longopts
        self.reconcilesorders = reconcilesorders
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
        ans["expandsabbr"] = self.expandsabbr
        ans["is_posix"] = self.is_posix
        ans["longopts"] = self.longopts
        ans["reconcilesorders"] = self.reconcilesorders
        ans["shortopts"] = self.shortopts
        ans["special"] = self.special
        return ans

    @property
    def bundling(self: Self, /) -> Tuning:
        "This property decides how to approach the bundling of short options."
        return self._bundling

    @bundling.setter
    def bundling(self: Self, value: int | NotImplementedType, /) -> None:
        "This property decides how to approach the bundling of short options."
        if isinstance(value, NotImplementedType):
            return
        self._bundling = Tuning(value)

    @setdoc.basic
    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def expandsabbr(self: Self, /) -> bool:
        return self._expandsabbr

    @expandsabbr.setter
    def expandsabbr(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._expandsabbr = bool(value)

    @property
    def is_posix(self: Self, /) -> bool:
        return self._is_posix

    @is_posix.setter
    def is_posix(
        self: Self, value: SupportsBool | Infer | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        if isinstance(value, Infer):
            self._is_posix = "POSIXLY_CORRECT" in os.environ
        else:
            self._is_posix = bool(value)

    @property
    def longopts(self: Self, /) -> tuple[str, ...] | None:
        """getopt-style long options; None disables long-option parsing."""
        return self._longopts

    @longopts.setter
    def longopts(
        self: Self, value: tuple[object, ...] | None | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        if value is None:
            self._longopts = None
        else:
            self._longopts = tuple(map(str, value))

    def parse_args(
        self: Self,
        args: Optional[Iterable[object]] = None,
    ) -> tuple[list[str], list[Message]]:
        "This method parses args."
        return process(
            args,
            **self._dict(),
        )

    @property
    def reconcilesorders(self: Self, /) -> bool:
        return self._reconcilesorders

    @reconcilesorders.setter
    def reconcilesorders(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._reconcilesorders = bool(value)

    @property
    def shortopts(self: Self, /) -> str | None:
        """getopt-style short options; None disables short-option parsing."""
        return self._shortopts

    @shortopts.setter
    def shortopts(self: Self, value: object, /) -> None:
        if isinstance(value, NotImplementedType):
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
    def special(self: Self, value: int | NotImplementedType, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        if isinstance(value, NotImplementedType):
            return
        self._special = Tuning(value)

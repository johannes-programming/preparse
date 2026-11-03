from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
import sys
from collections.abc import Iterable
from types import NotImplementedType
from typing import Any, Optional, Self

from preparse._processing import process
from preparse.abc.Copyable import Copyable
from preparse.abc.Message import Message
from preparse.enum.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool


class PreParser(Copyable):

    __slots__ = (
        "_shortsopts",
        "_longopts",
        "_bundling",
        "_expandsabbr",
        "_expectsabbr",
        "_expectsposix",
        "_prog",
        "_reconcilesorders",
        "_special",
    )
    _shortsopts: str | None
    _longopts: tuple[str, ...] | None
    _bundling: Tuning
    _expandsabbr: bool
    _expectsabbr: bool
    _expectsposix: bool
    _prog: str
    _reconcilesorders: bool
    _special: Tuning

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, PreParser):
            return self.todict() == other.todict()
        else:
            return NotImplemented

    def __init__(
        self: Self,
        other: PreParser | NotImplementedType = NotImplemented,
        /,
        *,
        shortsopts: str | None | NotImplementedType = NotImplemented,
        longopts: tuple[str, ...] | None | NotImplementedType = NotImplemented,
        bundling: int | NotImplementedType = NotImplemented,
        expandsabbr: SupportsBool | NotImplementedType = NotImplemented,
        expectsabbr: SupportsBool | NotImplementedType = NotImplemented,
        expectsposix: SupportsBool | NotImplementedType = NotImplemented,
        prog: object = NotImplemented,
        reconcilesorders: SupportsBool | NotImplementedType = NotImplemented,
        special: int | NotImplementedType = NotImplemented,
    ) -> None:
        self._shortsopts = ""
        self._longopts = ()
        self._bundling = Tuning.MAINTAIN
        self._expandsabbr = True
        self._expectsabbr = True
        self._expectsposix = False
        self.prog = None
        self._reconcilesorders = True
        self._special = Tuning.MAINTAIN
        if not isinstance(other, NotImplementedType):
            self.shortsopts = other.shortsopts
            self.longopts = other.longopts
            self.bundling = other.bundling
            self.expandsabbr = other.expandsabbr
            self.expectsabbr = other.expectsabbr
            self.expectsposix = other.expectsposix
            self.prog = other.prog
            self.reconcilesorders = other.reconcilesorders
            self.special = other.special
        self.shortsopts = shortsopts
        self.longopts = longopts
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix
        self.prog = prog
        self.reconcilesorders = reconcilesorders
        self.special = special

    def __repr__(self: Self, /) -> str:
        return f"{type(self).__name__}(" + ", ".join(
            f"{name}={value!r}" for name, value in self.todict().items()
        ) + ")"

    @property
    def shortsopts(self: Self, /) -> str | None:
        """Short option characters, with ':' or '::' argument suffixes.

        None disables short option parsing; an empty string enables it but
        declares no valid short options.
        """
        return self._shortsopts

    @shortsopts.setter
    def shortsopts(self: Self, value: str | None | NotImplementedType, /) -> None:
        if isinstance(value, NotImplementedType):
            return
        if value is not None and not isinstance(value, str):
            raise TypeError("shortsopts must be a string or None")
        self._shortsopts = value

    @property
    def longopts(self: Self, /) -> tuple[str, ...] | None:
        """Getopt-style long names, with '=' or '==' argument suffixes.

        None disables long option parsing; an empty tuple enables it but
        declares no valid long options.
        """
        return self._longopts

    @longopts.setter
    def longopts(
        self: Self, value: tuple[str, ...] | None | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        if value is not None:
            if isinstance(value, str):
                raise TypeError("longopts must be a tuple of strings or None")
            value = tuple(value)
            if not all(isinstance(item, str) for item in value):
                raise TypeError("longopts must contain only strings")
        self._longopts = value

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
    def expectsabbr(self: Self, /) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    def expectsabbr(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self, /) -> bool:
        return self._expectsposix

    @expectsposix.setter
    def expectsposix(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        if value == "infer":
            self._expectsposix = "POSIXLY_CORRECT" in os.environ
        else:
            self._expectsposix = bool(value)

    def parse_args(
        self: Self,
        args: Optional[Iterable[object]] = None,
    ) -> tuple[list[str], list[Message]]:
        "This method parses args."
        return process(
            args,
            **self.todict(),
        )

    @property
    def prog(self: Self, /) -> str:
        "This property represents the name of the program."
        return self._prog

    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        "This property represents the name of the program."
        if isinstance(value, NotImplementedType):
            return
        if value is None:
            self._prog = str(os.path.basename(sys.argv[0]))
        else:
            self._prog = str(value)

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
    def special(self: Self, /) -> Tuning:
        "This Tuning property determines the approach towards the special argument."
        return self._special

    @special.setter
    def special(self: Self, value: int | NotImplementedType, /) -> None:
        "This Tuning property determines the approach towards the special argument."
        if isinstance(value, NotImplementedType):
            return
        self._special = Tuning(value)

    def todict(self: Self, /) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        ans: dict[str, Any]
        ans = dict()
        ans["shortsopts"] = self.shortsopts
        ans["longopts"] = self.longopts
        ans["bundling"] = self.bundling
        ans["expandsabbr"] = self.expandsabbr
        ans["expectsabbr"] = self.expectsabbr
        ans["expectsposix"] = self.expectsposix
        ans["prog"] = self.prog
        ans["reconcilesorders"] = self.reconcilesorders
        ans["special"] = self.special
        return ans

from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
import sys
from collections.abc import Hashable, Iterable
from types import NotImplementedType
from typing import Any, Optional, Self, TypeVar

import setdoc
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import process
from preparse.abc.Copyable import Copyable
from preparse.abc.Message import Message
from preparse.core.Optdict import Optdict
from preparse.enum.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem

Key = TypeVar("Key", bound=Hashable)


class PreParser(Copyable):

    __slots__ = (
        "_allowslong",
        "_allowsshort",
        "_bundling",
        "_expandsabbr",
        "_expectsabbr",
        "_expectsposix",
        "_optdict",
        "_prog",
        "_reconcilesorders",
        "_special",
    )
    _allowslong: bool
    _allowsshort: bool
    _bundling: Tuning
    _expandsabbr: bool
    _expectsabbr: bool
    _expectsposix: bool
    _optdict: Optdict
    _prog: str
    _reconcilesorders: bool
    _special: Tuning

    def __eq__(self: Self, other: object, /) -> bool | NotImplementedType:
        if isinstance(other, PreParser):
            return self.todict() == other.todict()
        else:
            return NotImplemented

    @setdoc.basic
    def __init__(
        self: Self,
        other: PreParser | NotImplementedType = NotImplemented,
        /,
        *,
        allowslong: SupportsBool | NotImplementedType = NotImplemented,
        allowsshort: SupportsBool | NotImplementedType = NotImplemented,
        bundling: int | NotImplementedType = NotImplemented,
        expandsabbr: SupportsBool | NotImplementedType = NotImplemented,
        expectsabbr: SupportsBool | NotImplementedType = NotImplemented,
        expectsposix: SupportsBool | NotImplementedType = NotImplemented,
        optdict: (
            SupportsKeysAndGetitem[Key, int | None]
            | Iterable[tuple[Key, int | None]]
            | NotImplementedType
        ) = NotImplemented,
        prog: object = NotImplemented,
        reconcilesorders: SupportsBool | NotImplementedType = NotImplemented,
        special: int | NotImplementedType = NotImplemented,
    ) -> None:
        self._allowslong = True
        self._allowsshort = True
        self._bundling = Tuning.MAINTAIN
        self._expandsabbr = True
        self._expectsabbr = True
        self._expectsposix = False
        self._optdict = Optdict()
        self.prog = None
        self._reconcilesorders = True
        self._special = Tuning.MAINTAIN
        if not isinstance(other, NotImplementedType):
            self.allowslong = other.allowslong
            self.allowsshort = other.allowsshort
            self.bundling = other.bundling
            self.expandsabbr = other.expandsabbr
            self.expectsabbr = other.expectsabbr
            self.expectsposix = other.expectsposix
            self.optdict = other.optdict
            self.prog = other.prog
            self.reconcilesorders = other.reconcilesorders
            self.special = other.special
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.bundling = bundling
        self.expandsabbr = expandsabbr
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix
        self.optdict = optdict
        self.prog = prog
        self.reconcilesorders = reconcilesorders
        self.special = special

    @setdoc.basic
    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self, /) -> bool:
        return self._allowslong

    @allowslong.setter
    def allowslong(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._allowslong = bool(value)

    @property
    def allowsshort(self: Self, /) -> bool:
        return self._allowsshort

    @allowsshort.setter
    def allowsshort(
        self: Self, value: SupportsBool | NotImplementedType, /
    ) -> None:
        if isinstance(value, NotImplementedType):
            return
        self._allowsshort = bool(value)

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

    @property
    def optdict(self: Self, /) -> Optdict:
        "This property gives a dictionary of options."
        return self._optdict

    @optdict.setter
    def optdict(self: Self, value: Any, /) -> None:
        "This property gives a dictionary of options."
        value_: Optdict
        if isinstance(value, NotImplementedType):
            return
        value_ = Optdict(value)
        self._optdict.clear()
        self._optdict.update(value_)

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
        ans["allowslong"] = self.allowslong
        ans["allowsshort"] = self.allowsshort
        ans["bundling"] = self.bundling
        ans["expandsabbr"] = self.expandsabbr
        ans["expectsabbr"] = self.expectsabbr
        ans["expectsposix"] = self.expectsposix
        ans["optdict"] = self.optdict
        ans["prog"] = self.prog
        ans["reconcilesorders"] = self.reconcilesorders
        ans["special"] = self.special
        return ans

from __future__ import annotations

__all__: list[str] = ["FrameworkSettings"]

import os
import sys
from collections.abc import Callable, Hashable, Iterable
from typing import Any, Optional, Self

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import process
from preparse.core.Click import Click
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsBool import SupportsBool
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from preparse.warnings.PreparseWarning import PreparseWarning


class FrameworkSettings(Copyable):

    __slots__ = (
        "_allowslong",
        "_allowsshort",
        "_expectsabbr",
        "_expectsposix",
    )

    @setdoc.basic
    def __init__(
        self: Self,
        *,
        allowslong: SupportsBool = True,
        allowsshort: SupportsBool = True,
        expectsabbr: SupportsBool = True,
        expectsposix: SupportsBool = False,
    ) -> None:
        self.allowslong = allowslong
        self.allowsshort = allowsshort
        self.expectsabbr = expectsabbr
        self.expectsposix = expectsposix

    @setdoc.basic
    def __repr__(self: Self) -> str:
        return datarepr(type(self).__name__, **self.todict())

    @property
    def allowslong(self: Self) -> bool:
        return self._allowslong

    @allowslong.setter
    def allowslong(self: Self, value: SupportsBool) -> None:
        self._allowslong = bool(value)

    @property
    def allowsshort(self: Self) -> bool:
        return self._allowsshort

    @allowsshort.setter
    def allowsshort(self: Self, value: SupportsBool) -> None:
        self._allowsshort = bool(value)

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(**self.todict())

    @property
    def expectsabbr(self: Self) -> bool:
        return self._expectsabbr

    @expectsabbr.setter
    def expectsabbr(self: Self, value: SupportsBool) -> None:
        self._expectsabbr = bool(value)

    @property
    def expectsposix(self: Self) -> bool:
        return self._expectsposix

    @expectsposix.setter
    def expectsposix(self: Self, value: SupportsBool) -> None:
        value_: Any
        if value == "infer":
            value_ = os.environ.get("POSIXLY_CORRECT")
        else:
            value_ = value
        self._expectsposix = bool(value_)

    def parse_args(
        self: Self,
        args: Optional[Iterable[object]] = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, **self.todict())

    def todict(self: Self) -> dict[str, Any]:
        "This method returns a dict representing the current instance."
        return dict(
            allowslong=self.allowslong,
            allowsshort=self.allowsshort,
            expectsabbr=self.expectsabbr,
            expectsposix=self.expectsposix,
        )

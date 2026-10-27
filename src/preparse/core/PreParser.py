from __future__ import annotations

__all__: list[str] = ["PreParser"]

import os
import sys
from collections.abc import Callable, Hashable, Iterable
from typing import Any, Optional, Self, cast

import click as cl
import setdoc
from copyable import Copyable
from datarepr import datarepr
from tofunc import tofunc

from preparse._processing import process
from preparse.core.Click import Click
from preparse.core.OptDict import OptDict
from preparse.core.FrameworkSettings import FrameworkSettings
from preparse.core.TransformationSettings import TransformationSettings
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem
from preparse.warnings.PreparseWarning import PreparseWarning
import dataclasses


class PreParser(Copyable):

    __slots__ = ("_frameworkSettings","_optDict", "_transformationSettings")

    frameworkSettings: FrameworkSettings
    optDict: OptDict
    transformationSettings: TransformationSettings

    def __init__(
        self: Self,
        other: PreParser | None,
        /,
        *,
        frameworkSettings: FrameworkSettings |None =None,
        optDict: SupportsKeysAndGetitem | Iterable[tuple[object, object]] |None= None,
        transformationSettings: TransformationSettings|None=None,
    ) -> None:
        self._init(
            other,
            frameworkSettings=frameworkSettings,
            optDict=optDict,
            transformationSettings=transformationSettings,
        )

    def __repr__(self: Self, /) -> str:
        return datarepr(type(self).__name__, **self.todict())
    
    def _init(
        self: Self,
        other: PreParser |None,
        /,
        *,
        frameworkSettings: FrameworkSettings |None,
        optDict: SupportsKeysAndGetitem | Iterable[tuple[object, object]] | None,
        transformationSettings: TransformationSettings|None,
    ) -> None:
        if other is None or frameworkSettings is not None:
            self._frameworkSettings=FrameworkSettings(frameworkSettings)
        else:
            self._frameworkSettings=FrameworkSettings(other.frameworkSettings)
        if other is None or optDict is not None:
            self._optDict=OptDict(optDict)
        else:
            self._optDict=OptDict(other.optDict)
        if other is None or transformationSettings is not None:
            self._transformationSettings=TransformationSettings(transformationSettings)
        else:
            self._transformationSettings=TransformationSettings(other.transformationSettings)


    def click(self: Self, /, cmd: object = True, ctx: object = True) -> Click:
        "This method returns a decorator that infuses the current instance into parse_args."
        return Click(parser=self, cmd=cmd, ctx=ctx)

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def frameworkSettings(self: Self, /) -> FrameworkSettings:
        return self._frameworkSettings
    @frameworkSettings.setter
    def frameworkSettings(self:Self, value: FrameworkSettings, /) -> None:
        self._frameworkSettings._init(value)

    @property
    def optDict(self: Self, /) -> OptDict:
        return self._optDict
    @optDict.setter
    def optDict(self:Self, value: OptDict, /) -> None:
        self._optDict._init(value)

    def parse_args(
        self: Self, 
        /,
        args: Iterable[object] | None = None,
    ) -> list[str]:
        "This method parses args."
        return process(args, self)

    @property
    def transformationSettings(self: Self, /) -> TransformationSettings:
        return self._transformationSettings
    @transformationSettings.setter
    def transformationSettings(self:Self, value: TransformationSettings, /) -> None:
        self._transformationSettings._init(value)


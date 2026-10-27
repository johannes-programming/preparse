__all__:list[str]=["TransformationSettings"]

import dataclasses
from preparse.enums.Tuning import Tuning
from collections.abc import Sized, Callable
from tofunc import tofunc

type SupportsBool = Sized | int

class TransformationSettings:

    __slots__ = (

        "_bundling",
        "_expandsabbr",
        "_prog",
        "_reconcilesorders",
        "_special",
        "_warn",
    )

    def __init__(
        self: Self, 
        other: TransformationSettings |None= None, 
        /, 
        *, 
        bundling: object = Tuning.MAINTAIN,
        expandsabbr: object = True,
        prog: object = None,
        reconcilesorders: object = True,
        special: object = Tuning.MAINTAIN,
        warn: Callable[[PreparseWarning], Any] | None = str,
    ) -> None:
        self._init(
            other,
            bundling=bundling,
            expandsabbr=expandsabbr,
            prog=prog,
            reconcilesorders=reconcilesorders,
            special=special,
            warn=warn,
        )
    
    def _init(
        self: Self, 
        other: TransformationSettings |None, 
        /, 
        *, 
        bundling: object,
        expandsabbr: object,
        prog: object,
        reconcilesorders: object,
        special: object,
        warn: Callable[[PreparseWarning], Any],
    ) -> None:
        if other is None or bundling is not None:
            self._frameworkSettings=FrameworkSettings(frameworkSettings)
        else:
            self._frameworkSettings=FrameworkSettings(other.frameworkSettings)

    @property
    def bundling(self: Self, /) -> Tuning:
        return self._bundling
    @bundling.setter
    def bundling(self: Self, value: object, /) -> None:
        self._bundling = Tuning(value)

    @property
    def expandsabbr(self: Self, /) -> bool:
        return self._expandsabbr
    @expandsabbr.setter
    def expandsabbr(self: Self, value: SupportsBool, /) -> None:
        self._expandsabbr = bool(value)

    @property
    def prog(self: Self, /) -> bool:
        return self._prog
    @prog.setter
    def prog(self: Self, value: object, /) -> None:
        self._prog = str(sys.argv[0] if value is None else value)

    @property
    def reconcilesorders(self: Self, /) -> bool:
        return self._reconcilesorders
    @reconcilesorders.setter
    def reconcilesorders(self: Self, value: SupportsBool, /) -> None:
        self._reconcilesorders = bool(value)

    @property
    def special(self: Self, /) -> Tuning:
        return self._special
    @special.setter
    def special(self: Self, value: object, /) -> None:
        self._special = Tuning(value)

    @property
    def warn(self: Self, /) -> Callable[[Any], str]:
        return self._warn
    @warn.setter
    def warn(self: Self, value: Callable[[Any], str], /) -> None:
        self._warn = tofunc(value)
    

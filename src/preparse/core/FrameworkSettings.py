__all__:list[str]=["FrameworkSettings"]

from collections.abc import Sized

type SupportsBool = Sized| int

class FrameworkSettings:

    __slots__ = (
        "_allowslong",
        "_allowsshort",
        "_expectsabbr",
        "_expectsposix",
    )

    @property
    def allowslong(self:Self, /) -> bool:
        return self._allowslong
    @allowslong.setter
    def allowslong(self: Self, value: SupportsBool,/) -> None:
        self._allowslong = bool(value)

    @property
    def allowsshort(self:Self, /) -> bool:
        return self._allowsshort
    @allowsshort.setter
    def allowsshort(self: Self, value: SupportsBool,/) -> None:
        self._allowsshort = bool(value)

    @property
    def expectsabbr(self:Self, /) -> bool:
        return self._expectsabbr
    @expectsabbr.setter
    def expectsabbr(self: Self, value: SupportsBool,/) -> None:
        self._expectsabbr = bool(value)

    @property
    def expectsposix(self:Self, /) -> bool:
        return self._expectsposix
    @expectsposix.setter
    def expectsposix(self: Self, value: SupportsBool,/) -> None:
        self._expectsposix = bool(value)




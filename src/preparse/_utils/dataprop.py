from typing import *
from namings import Naming

__all__ = ["dataprop"]


def dataprop(func: Callable) -> property:
    "This magic method implements calling the current instance."

    def fget(self: Self) -> Any:
        return self._data[func.__name__]

    def fset(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", Naming())
        self._data[func.__name__] = func(self, value)

    kwargs: Naming
    kwargs = Naming()
    kwargs["doc"] = func.__doc__
    kwargs["fget"] = fget
    kwargs["fset"] = fset
    return property(**kwargs)

from typing import *

import namings

__all__ = ["dataprop"]


def dataprop(func: Callable) -> property:
    "This magic method implements calling the current instance."

    def fget(self: Self) -> Any:
        return self._data[func.__name__]

    def fset(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", namings.Naming())
        self._data[func.__name__] = func(self, value)

    kwargs: namings.Naming
    kwargs = namings.Naming()
    kwargs["doc"] = func.__doc__
    kwargs["fget"] = fget
    kwargs["fset"] = fset
    return property(**kwargs)

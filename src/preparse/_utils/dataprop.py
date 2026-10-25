__all__: list[str] = ["dataprop"]

from collections.abc import Callable
from typing import Any, Self


def dataprop(func: Callable[..., Any]) -> property:
    "This magic method implements calling the current instance."

    kwargs: dict[str, Any]

    def fget(self: Self) -> Any:
        return self._data[func.__name__]

    def fset(self: Self, value: Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data[func.__name__] = func(self, value)

    kwargs = dict()
    kwargs["doc"] = func.__doc__
    kwargs["fget"] = fget
    kwargs["fset"] = fset
    return property(**kwargs)

from typing import *
import inspect as ins

__all__ = ["dataprop", "dataslot"]


def dataprop(func: Callable) -> property:
    "This magic method implements calling the current instance."
    def fget(self:Self) -> Any:
        return self._data[func.__name__]
    def fset(self:Self, value:Any) -> None:
        self._data = getattr(self, "_data", dict())
        self._data[func.__name__] = func(self, value)
    kwargs:dict = dict()
    kwargs["doc"] = func.__doc__
    kwargs["fget"] = fget
    kwargs["fset"] = fset
    ans = property(**kwargs)
    return ans

def dataslot(cls:type)->type:
    cls.__slots__ = ("_data",)
    k:Any
    v:Any
    d:dict = dict()
    for k, v in cls.__dict__.items():
        if ins.isfunction(v):
            d[k] = v
    for k, v in d.items():
        setattr(cls, k, dataprop(v))
    return cls
    


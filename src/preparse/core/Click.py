from __future__ import annotations

import dataclasses
import functools
import types
from typing import *

import setdoc
from copyable import Copyable

if TYPE_CHECKING:
    from .PreParser import PreParser

__all__ = ["Click"]


@dataclasses.dataclass
class Click(Copyable):

    parser: PreParser
    cmd: Any = True
    ctx: Any = True

    def __call__(self: Self, target: Any) -> Any:
        "This magic method implements self(target)."
        if isinstance(target, types.FunctionType):
            return self._call_function(target)
        if isinstance(target, types.MethodType):
            return self._call_method(target)
        return self._call_other(target)

    def _call_function(self: Self, target: types.FunctionType) -> types.FunctionType:
        @functools.wraps(target)
        def ans(cmd: Any, ctx: Any, args: Any) -> Any:
            p: Any
            p = self.parser.copy()
            if self.cmd:
                p.reflectClickCommand(cmd)
            if self.ctx:
                p.reflectClickContext(ctx)
            return target(cmd, ctx, p.parse_args(args))

        return ans

    def _call_method(self: Self, target: types.MethodType) -> types.MethodType:
        func: Callable
        func = self(target.__func__)
        return types.MethodType(func, target.__self__)

    def _call_other(self: Self, target: Any) -> Any:
        target.parse_args = self(target.parse_args)
        return target

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(parser=self.parser, cmd=self.cmd, ctx=self.ctx)

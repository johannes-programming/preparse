from __future__ import annotations

__all__: list[str] = ["Click"]

import dataclasses
import functools
import types
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Self

import overloadable
import setdoc
from copyable import Copyable

if TYPE_CHECKING:
    from .PreParser import PreParser


@dataclasses.dataclass
class Click(Copyable):

    parser: PreParser
    cmd: Any = True
    ctx: Any = True

    @overloadable.Overloadable
    def __call__(self: Self, target: Any) -> Any:
        "This magic method implements self(target)."
        if isinstance(target, types.FunctionType):
            return "function"
        if isinstance(target, types.MethodType):
            return "method"
        return "other"

    @__call__.overload("function")
    def __call__(self: Self, target: types.FunctionType) -> types.FunctionType:
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

    @__call__.overload("method")
    def __call__(self: Self, target: types.MethodType) -> types.MethodType:
        func: Callable[..., Any]
        func = self(target.__func__)
        return types.MethodType(func, target.__self__)

    @__call__.overload("other")
    def __call__(self: Self, target: Any) -> Any:
        target.parse_args = self(target.parse_args)
        return target

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(parser=self.parser, cmd=self.cmd, ctx=self.ctx)

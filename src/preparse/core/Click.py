from __future__ import annotations

import dataclasses
import functools
from collections.abc import Callable
from types import FunctionType, MethodType
from typing import TYPE_CHECKING, Any, Self, TypeVar, overload

import setdoc
from copyable import Copyable

from ..typing.Parser import Parser

if TYPE_CHECKING:
    from .PreParser import PreParser

__all__ = ["Click"]


ParserTarget = TypeVar("Parser", bound=Parser)


@dataclasses.dataclass
class Click(Copyable):

    parser: PreParser
    cmd: object = True
    ctx: object = True

    @overload
    def __call__(self: Self, target: FunctionType) -> FunctionType:
        "This magic method implements self(target)."
        ...

    @overload
    def __call__(self: Self, target: MethodType) -> MethodType:
        "This magic method implements self(target)."
        ...

    @overload
    def __call__(self: Self, target: ParserTarget) -> ParserTarget:
        "This magic method implements self(target)."
        ...

    def __call__(
        self: Self,
        target: FunctionType | MethodType | ParserTarget,
    ) -> FunctionType | MethodType | ParserTarget:
        "This magic method implements self(target)."
        if isinstance(target, FunctionType):
            return self._call_function(target)
        if isinstance(target, MethodType):
            return self._call_method(target)
        return self._call_other(target)

    def _call_function(self: Self, target: FunctionType) -> FunctionType:
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

    def _call_method(self: Self, target: MethodType) -> MethodType:
        func: Callable[..., Any]
        func = self(target.__func__)
        return MethodType(func, target.__self__)

    def _call_other(self: Self, target: Parser) -> Parser:
        target.parse_args = self(target.parse_args)
        return target

    @setdoc.basic
    def copy(self: Self) -> Self:
        return type(self)(parser=self.parser, cmd=self.cmd, ctx=self.ctx)

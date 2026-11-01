"""Support Enum() as shorthand for Enum(None), without adding members."""

from enum import EnumType


class DefaultedEnumType(EnumType):
    def __call__(cls, value=None, *args, **kwargs):
        return super().__call__(value, *args, **kwargs)

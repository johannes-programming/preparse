__all__: list[str] = ["PreparseRequiredArgumentWarning"]

from typing import Self

from preparse.warnings.PreparseDualWarning import PreparseDualWarning


class PreparseRequiredArgumentWarning(PreparseDualWarning):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "option '%s' requires an argument"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "option requires an argument -- '%s'"

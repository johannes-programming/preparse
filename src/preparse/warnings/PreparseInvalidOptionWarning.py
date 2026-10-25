from typing import Self

from preparse.warnings.PreparseDualWarning import PreparseDualWarning

__all__ = ["PreparseInvalidOptionWarning"]


class PreparseInvalidOptionWarning(PreparseDualWarning):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "unrecognized option '%s'"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "invalid option -- '%s'"

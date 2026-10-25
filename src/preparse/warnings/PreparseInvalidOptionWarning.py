__all__: list[str] = ["PreparseInvalidOptionWarning"]

from typing import Self

from preparse.warnings.PreparseDualWarning import PreparseDualWarning


class PreparseInvalidOptionWarning(PreparseDualWarning):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "unrecognized option '%s'"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "invalid option -- '%s'"

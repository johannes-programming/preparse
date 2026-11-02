__all__: list[str] = ["RequiredArgumentMessage"]

from typing import Self

from preparse.abc.DualMessage import DualMessage


class RequiredArgumentMessage(DualMessage):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "option '%s' requires an argument"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "option requires an argument -- '%s'"

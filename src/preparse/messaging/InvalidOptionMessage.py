__all__: list[str] = ["InvalidOptionMessage"]

from typing import Self

from preparse.abc.DualMessage import DualMessage


class InvalidOptionMessage(DualMessage):

    @classmethod
    def _longmsg(cls: type[Self]) -> str:
        return "unrecognized option '%s'"

    @classmethod
    def _shortmsg(cls: type[Self]) -> str:
        return "invalid option -- '%s'"

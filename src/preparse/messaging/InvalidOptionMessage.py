__all__: list[str] = ["InvalidOptionMessage"]

from preparse.abc.DualMessage import DualMessage


class InvalidOptionMessage(DualMessage):

    __slots__ = ()

    @staticmethod
    def _longmsg() -> str:
        return "unrecognized option '%s'"

    @staticmethod
    def _shortmsg() -> str:
        return "invalid option -- '%s'"

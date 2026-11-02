__all__: list[str] = ["RequiredArgumentMessage"]


from preparse.abc.DualMessage import DualMessage


class RequiredArgumentMessage(DualMessage):
    __slots__ = ()

    @staticmethod
    def _longmsg() -> str:
        return "option '%s' requires an argument"

    @staticmethod
    def _shortmsg() -> str:
        return "option requires an argument -- '%s'"

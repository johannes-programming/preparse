__all__: list[str] = ["LongonlyMessage"]

from preparse.abc.Message import Message


class LongonlyMessage(Message):
    pass  # only possible for long options

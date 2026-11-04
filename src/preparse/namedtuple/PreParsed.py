__all__: list[str] = ["PreParsed"]

from typing import NamedTuple

from preparse.abc.Message import Message


class PreParsed(NamedTuple):
    args: list[str]
    messages: list[Message]

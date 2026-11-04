__all__: list[str] = ["Reserve"]

from typing import NamedTuple


class Reserve(NamedTuple):
    joined: bool
    arg: str

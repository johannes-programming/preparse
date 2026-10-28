__all__: list[str] = ["SupportsBool"]
from collections.abc import Sized
from typing import TypeAlias

SupportsBool: TypeAlias = Sized | int

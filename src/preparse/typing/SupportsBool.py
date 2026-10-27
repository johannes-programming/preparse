__all__: list[str] = ["SupportsBool"]

from collections.abc import Sized

type SupportsBool = Sized | int

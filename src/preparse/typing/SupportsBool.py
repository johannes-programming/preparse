from __future__ import annotations

__all__: list[str] = ["SupportsBool"]

from collections.abc import Sized
from typing import SupportsIndex, TypeAlias

SupportsBool: TypeAlias = Sized | SupportsIndex | None

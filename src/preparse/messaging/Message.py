from __future__ import annotations

__all__: list[str] = ["Message"]


from abc import ABC, abstractmethod
from typing import Self


class Message(ABC):
    """Abstract base of structured preparsing diagnostics."""

    @abstractmethod
    def oneliner(self: Self, /) -> str:
        """Return a one-line getopt-style description."""

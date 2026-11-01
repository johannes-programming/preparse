"""Getopt-style command-line argument preparsing and diagnostics."""

__all__: list[str] = [
    "PreParser",
    "Framework",
    "OptList",
    "Transformation",
]
from .core.Framework import Framework
from .core.OptList import OptList
from .core.PreParser import PreParser
from .core.Transformation import Transformation

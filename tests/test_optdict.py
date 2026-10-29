__all__: list[str] = ["TestPreparse"]

import enum
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import Any, Self

from preparse import PreParser


class Utils(enum.Enum):
    utils = None

    @cached_property
    def data(sefl: Self) -> dict[str, Any]:
        text: str
        text = resources.read_text("preparse.tests", "secondary.toml")
        return tomllib.loads(text)


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        dublicate: PreParser.OptDict
        original: PreParser.OptDict
        original = PreParser.OptDict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self) -> None:
        data: dict[str, PreParser.OptDict.Nargs]
        original: PreParser.OptDict
        data = {
            "--foo": PreParser.OptDict.Nargs.NO_ARGUMENT,
            "-bar": PreParser.OptDict.Nargs.REQUIRED_ARGUMENT,
        }
        original = PreParser.OptDict(data)
        self.assertEqual(repr(original), f"PreParser.OptDict({data})")
        self.assertEqual(repr(original), str(original))
        self.assertEqual(repr(original), format(original))


if __name__ == "__main__":
    unittest.main()

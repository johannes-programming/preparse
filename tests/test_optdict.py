__all__: list[str] = ["TestPreparse"]

import enum
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from pathlib import Path
from typing import Any, Self

from preparse._tests.secondary import secondary
from preparse.core.Optdict import Optdict
from preparse.core.PreParser import PreParser
from preparse.enums.Nargs import Nargs


class Utils(enum.Enum):
    utils = None

    @cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load and return the shared TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent / "secondary.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        dublicate: Optdict
        original: Optdict
        original = Optdict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self) -> None:
        data: dict[str, Nargs]
        original: Optdict
        data = {"--foo": Nargs.NO_ARGUMENT, "-bar": Nargs.REQUIRED_ARGUMENT}
        original = Optdict(data)
        self.assertEqual(repr(original), f"Optdict({data})")
        self.assertEqual(repr(original), str(original))
        self.assertEqual(repr(original), format(original))

    def test_secondary(self: Self) -> None:
        parser: PreParser
        parser = PreParser()
        parser.reflectClickCommand(secondary)
        self.assertEqual(
            tuple(parser.optdict.items()),
            tuple(Utils.utils.data["optdict"].items()),
        )


if __name__ == "__main__":
    unittest.main()

import enum
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import Any, Self

from preparse._tests.secondary import secondary
from preparse.core.Optdict import Optdict
from preparse.core.PreParser import PreParser
from preparse.enums.Nargs import Nargs

__all__ = ["TestPreparse"]


class Utils(enum.Enum):
    utils = None

    @cached_property
    def data(sefl: Self) -> dict[str, Any]:
        text: str
        text = resources.read_text("preparse.tests", "secondary.toml")
        return tomllib.loads(text)


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        original: Optdict
        dublicate: Optdict
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

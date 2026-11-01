__all__: list[str] = ["TestPreparse"]

import unittest
from typing import Self

from preparse.core.OptList import OptList
from preparse.enum.Nargs import Nargs


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        dublicate: OptList
        original: OptList
        original = OptList({"--foo": 0, "-bar": 1}.items())
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self) -> None:
        data: dict[str, Nargs]
        original: OptList
        data = {"--foo": Nargs.NO_ARGUMENT, "-bar": Nargs.REQUIRED_ARGUMENT}
        original = OptList(data.items())
        self.assertEqual(repr(original), f"OptList({list(data.items())})")
        self.assertEqual(repr(original), str(original))
        self.assertEqual(repr(original), format(original))


if __name__ == "__main__":
    unittest.main()

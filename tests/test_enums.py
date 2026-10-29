__all__: list[str] = ["TestEnums"]

import unittest
from typing import Self

from preparse import PreParser


class TestEnums(unittest.TestCase):

    def test_nargs_enum(self: Self) -> None:
        self.assertEqual(PreParser.OptDict.Nargs.NO_ARGUMENT, 0)
        self.assertEqual(PreParser.OptDict.Nargs.REQUIRED_ARGUMENT, 1)
        self.assertEqual(PreParser.OptDict.Nargs.OPTIONAL_ARGUMENT, 2)


if __name__ == "__main__":
    unittest.main()

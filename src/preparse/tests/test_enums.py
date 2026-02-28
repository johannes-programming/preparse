import unittest
from typing import *

from preparse.core.enums import *

__all__ = ["TestEnums"]


class TestEnums(unittest.TestCase):

    def test_nargs_enum(self: Self) -> None:
        self.assertEqual(Nargs.NO_ARGUMENT, 0)
        self.assertEqual(Nargs.REQUIRED_ARGUMENT, 1)
        self.assertEqual(Nargs.OPTIONAL_ARGUMENT, 2)


if __name__ == "__main__":
    unittest.main()

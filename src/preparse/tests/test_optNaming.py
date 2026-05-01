import unittest
from typing import *

from preparse.core.enums import *
from preparse.core.OptNaming import OptNaming
from preparse.core.PreparseWarning import *

__all__ = ["TestPreparse"]


class TestPreparse(unittest.TestCase):

    def test_optNaming_copy(self: Self) -> None:
        original: OptNaming
        dublicate: OptNaming
        original = OptNaming({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)


if __name__ == "__main__":
    unittest.main()

import unittest
from typing import *

from preparse.core.enums import *
from preparse.core.OptDict import OptDict
from preparse.core.warnings import *

__all__ = ["TestPreparse"]


class TestPreparse(unittest.TestCase):

    def test_optDict_copy(self: Self) -> None:
        original: OptDict
        dublicate: OptDict
        original = OptDict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)


if __name__ == "__main__":
    unittest.main()

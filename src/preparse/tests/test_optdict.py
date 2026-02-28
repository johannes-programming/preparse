import unittest
from typing import *

from preparse.core.Click import Click
from preparse.core.enums import *
from preparse.core.Optdict import Optdict
from preparse.core.PreParser import PreParser
from preparse.core.warnings import *

__all__ = ["TestPreparse"]


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        original: Optdict
        dublicate: Optdict
        original = Optdict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)


if __name__ == "__main__":
    unittest.main()

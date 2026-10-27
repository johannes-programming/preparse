__all__: list[str] = ["TestPreparse"]

import unittest
from typing import Self

from preparse.core.Optdict import Optdict


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        dublicate: Optdict
        original: Optdict
        original = Optdict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)


if __name__ == "__main__":
    unittest.main()

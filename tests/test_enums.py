__all__: list[str] = ["TestEnums"]

import unittest
from typing import Self

from preparse.enum.Tuning import Tuning


class TestEnums(unittest.TestCase):
    def test_tuning_enum(self: Self) -> None:
        self.assertEqual(Tuning.MINIMIZE, 0)
        self.assertEqual(Tuning.MAXIMIZE, 1)
        self.assertEqual(Tuning.MAINTAIN, 2)


if __name__ == "__main__":
    unittest.main()

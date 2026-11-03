import unittest
from preparse.enum.Tuning import Tuning


class TestEnums(unittest.TestCase):
    def test_tuning(self) -> None:
        self.assertEqual((Tuning.MINIMIZE, Tuning.MAXIMIZE, Tuning.MAINTAIN), (0, 1, 2))
        self.assertIs(Tuning(777), Tuning.MAINTAIN)

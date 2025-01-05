import unittest
from preparse.core import LongOptionAbbreviations, Nargs, ShortOptionClusters

INVALID_VALUES = [-1, 3, 42, 100, 9999, "hello"]

class TestBaseEnum(unittest.TestCase):
    def test_missing_returns_value_2(self):
        # Define the subclasses to test
        subclasses = [LongOptionAbbreviations, Nargs, ShortOptionClusters]

        for subclass in subclasses:
            with self.subTest(subclass=subclass):
                # Test for values other than 0 and 1
                for invalid_value in INVALID_VALUES:
                    self.assertEqual(subclass(invalid_value), subclass(2),
                                     f"{subclass.__name__} did not return the expected value for {invalid_value}")

if __name__ == "__main__":
    unittest.main()
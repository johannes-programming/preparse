import unittest
from typing import Self

from preparse.core.Optdict import Optdict

__all__ = ["TestPreparse"]


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        original: Optdict
        dublicate: Optdict
        original = Optdict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self) -> None:
        data: dict[str, int]
        original: Optdict
        data = {"--foo": 0, "-bar": 1}
        original = Optdict(data)
        self.assertEqual(repr(original), f"Optdict({data})")
        self.assertEqual(repr(original), str(original))
        self.assertEqual(repr(original), format(original))


if __name__ == "__main__":
    unittest.main()

__all__: list[str] = ["TestPreparse"]

import unittest
from typing import Self

from preparse.core.OptDict import OptDict


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self) -> None:
        dublicate: OptDict
        original: OptDict
        original = OptDict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self) -> None:
        data: dict[str, OptDict.Nargs]
        original: OptDict
        data = {
            "--foo": OptDict.Nargs.NO_ARGUMENT,
            "-bar": OptDict.Nargs.REQUIRED_ARGUMENT,
        }
        original = OptDict(data)
        self.assertEqual(repr(original), f"OptDict({data})")
        self.assertEqual(repr(original), str(original))
        self.assertEqual(repr(original), format(original))


if __name__ == "__main__":
    unittest.main()

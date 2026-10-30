__all__: list[str] = ["TestPreparse"]

import unittest
from collections.abc import Iterable
from typing import Iterator, Self, TypeVar

from preparse.core.OptDict import OptDict

Item = TypeVar("Item")


class Foo:
    def __iter__(self: Self, /) -> Iterator[tuple[float, float]]:
        yield 1.25, 1.75
        yield 2.25, 2.75
        yield 3.25, 3.75

    def keys(self: Self, /) -> Iterable[int]:
        return list(range(5))


class TestPreparse(unittest.TestCase):

    def test_optdict_copy(self: Self, /) -> None:
        dublicate: OptDict
        original: OptDict
        original = OptDict({"--foo": 0, "-bar": 1})
        dublicate = original.copy()
        self.assertEqual(original, dublicate)

    def test_optdict_repr(self: Self, /) -> None:
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

    def test_optdict_SupportsKeys(self: Self) -> None:
        original: OptDict
        original = OptDict(Foo())


if __name__ == "__main__":
    unittest.main()

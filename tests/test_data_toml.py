__all__: list[str] = ["TestDataToml"]

import enum
import functools
import io
import math
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

from preparse.core.PreParser import PreParser


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load the converted TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)

    @staticmethod
    def testvalue(x: Any) -> Any:
        if not isinstance(x, float):
            return x
        if not math.isnan(x):
            return x
        return None


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        kwargs: dict[str, Any]
        name: str
        kwargs_: Any
        x: Any
        y: Any
        for name, kwargs in Utils.utils.data.items():
            kwargs_ = dict()
            for x, y in kwargs.items():
                kwargs_[x] = Utils.testvalue(y)
            with self.subTest(msg=name, **kwargs_):
                self.parse(**kwargs_)

    def parse(
        self: Self,
        /,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        answer: list[Any]
        erranswer: list[Any]
        parser: PreParser
        superanswer: list[Any]

        messages: Any
        parser = PreParser(**kwargs)
        answer, messages = parser.parse_args(query)
        erranswer = list(map(str, messages))
        superanswer = parser.parse_args(answer)[0]
        self.assertEqual(answer, superanswer, msg="idempotence failed!")
        self.assertEqual(answer, solution, msg="wrong answer!")
        if warnings is None:
            return
        self.assertEqual(erranswer, warnings, msg="wrong messages!")


if __name__ == "__main__":
    unittest.main()

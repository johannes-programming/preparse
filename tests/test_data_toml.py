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
from preparse.messaging.RequiredArgumentMessage import RequiredArgumentMessage


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
        erranswer: list[Any]
        parser: PreParser

        parser = PreParser(**kwargs)
        preParsed_a = parser.parse_args(query)
        preParsed_b = parser.parse_args(preParsed_a.args)
        if warnings is not None:
            erranswer = list(map(str, preParsed_a.messages))
            self.assertEqual(erranswer, warnings, msg="wrong messages!")
        self.assertEqual(preParsed_a.args, solution, msg="wrong answer!")
        if RequiredArgumentMessage in map(type, preParsed_a.messages):
            self.assertIsInstance(
                preParsed_a.messages.pop(0),
                RequiredArgumentMessage,
            )
        self.assertEqual(
            preParsed_a,
            preParsed_b,
            msg="idempotence failed!",
        )


if __name__ == "__main__":
    unittest.main()

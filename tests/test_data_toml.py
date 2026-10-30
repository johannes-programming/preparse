__all__: list[str] = ["TestDataToml"]

import enum
import functools
import io
import math
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

from preparse import PreParser


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load and return the shared TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)

    @staticmethod
    def istestable(x: Any) -> bool:
        if not isinstance(x, float):
            return True
        if not math.isnan(x):
            return True
        return False


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        kwargs: dict[str, Any]
        name: str
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)

    def parse(
        self: Self,
        *,
        testing: dict[str, Any],
        legacy: dict[str, Any],
        optDict: dict[str, Any],
        transformation: dict[str, Any],
        framework: dict[str, Any],
    ) -> None:
        answer: list[Any]
        erranswer: list[Any]
        parser: PreParser
        superanswer: list[Any]

        query: Any
        solution: Any
        warnings: Any

        query = testing["query"]
        solution = testing["solution"]
        warnings = testing["warnings"]
        self.assertEqual(len(testing), 3)

        parser = PreParser()
        parser.framework = PreParser.Framework(**framework)
        parser.optDict = optDict
        transformation_ = dict(transformation)
        if isinstance(transformation.get("depletion"), list):
            transformation_["depletion"] = PreParser.Transformation.Depletion[
                transformation["depletion"][0]
            ]
        parser.transformation = PreParser.Transformation(**transformation_)
        answer, messages = parser.parse_args(query)
        erranswer = [x.oneliner() for x in messages]
        superanswer = parser.parse_args(answer)[0]
        self.assertEqual(answer, superanswer, msg="idempotency failed!")
        self.assertEqual(
            answer, solution, msg="answer does not match solution!"
        )
        if not Utils.utils.istestable(warnings):
            return
        self.assertEqual(erranswer, warnings, msg="warnings faulty!")


if __name__ == "__main__":
    unittest.main()

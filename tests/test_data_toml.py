__all__: list[str] = ["TestDataToml"]

import enum
import functools
import io
import math
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

from preparse.core.Framework import Framework
from preparse.core.PreParser import PreParser
from preparse.core.Transformation import Transformation
from preparse.enum.Depletion import Depletion


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
        framework: dict[str, Any],
        transformation: dict[str, Any],
        optList: dict[str, Any],
    ) -> None:
        answer: list[Any]
        erranswer: list[Any]
        parser: PreParser
        superanswer: list[Any]

        transformation_ = dict(transformation)
        if isinstance(transformation["depletion"], str):
            transformation_["depletion"] = Depletion[
                transformation["depletion"]
            ]
        else:
            transformation_["depletion"] = tuple(transformation["depletion"])

        parser = PreParser(
            framework=Framework(**framework),
            optList=optList.items(),
            transformation=Transformation(**transformation_),
        )
        answer, messages = parser.parse_args(testing["query"])
        erranswer = [str(m) for m in messages]
        superanswer = parser.parse_args(answer)[0]
        self.assertEqual(answer, superanswer)
        self.assertEqual(answer, testing["solution"])
        if Utils.utils.istestable(testing["messages"]):
            self.assertEqual(erranswer, testing["messages"])


if __name__ == "__main__":
    unittest.main()

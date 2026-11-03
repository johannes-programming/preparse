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
        for name, kwargs in Utils.utils.data.items():
            kwargs_ = dict()
            for x, y in kwargs.items():
                kwargs_[x] = Utils.testvalue(y)
            with self.subTest(msg=name, **kwargs_):
                self.parse(**kwargs_)

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        answer: list[Any]
        data: dict[str, Any]
        erranswer: list[Any]
        msg: str
        parser: PreParser
        superanswer: list[Any]

        # TOML arrays become lists; TOML `false` stands for Python None,
        # which disables the corresponding option syntax in PreParser.
        parser = PreParser(**kwargs)
        data = dict(
            query=query,
            solution=solution,
            warnings=warnings,
            **kwargs,
        )
        answer, messages = parser.parse_args(query)
        erranswer = list(map(str, messages))
        superanswer = parser.parse_args(answer)[0]
        msg = "\n\ndata=%s,\nanswer=%s,\nsuperanswer=%s,\n\n" % (
            data,
            answer,
            superanswer,
        )
        self.assertEqual(answer, superanswer, msg=msg)
        msg = "\n\ndata=%s,\nanswer=%s,\nsolution=%s,\n\n" % (
            data,
            answer,
            solution,
        )
        self.assertEqual(answer, solution, msg=msg)
        if warnings is None:
            return
        msg = "\n\ndata=%s,\nerranswer=%s,\nwarnings=%s,\n\n" % (
            data,
            erranswer,
            warnings,
        )
        self.assertEqual(erranswer, warnings, msg=msg)


if __name__ == "__main__":
    unittest.main()

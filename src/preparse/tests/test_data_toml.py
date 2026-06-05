import enum
import math
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import Any, Self

from preparse.core.PreParser import PreParser

__all__ = ["TestDataToml"]


class Utils(enum.Enum):
    utils = None

    @cached_property
    def data(self: Self) -> dict[str, Any]:
        text: str
        text = resources.read_text("preparse.tests", "data.toml")
        return tomllib.loads(text)

    @staticmethod
    def istestable(x: Any) -> bool:
        if not isinstance(x, float):
            return True
        if not math.isnan(x):
            return True
        return False


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        name: str
        kwargs: dict[str, Any]
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        answer: list[Any]
        capture: list[Any]
        data: dict[str, Any]
        erranswer: list[Any]
        msg: str
        superanswer: list[Any]
        parser: PreParser
        capture = list()

        def warn(value: Any) -> None:
            capture.append(str(value))

        parser = PreParser(warn=warn, **kwargs)
        data = dict(
            query=query,
            solution=solution,
            warnings=warnings,
            **kwargs,
        )
        answer = parser.parse_args(query)
        erranswer = list(capture)
        superanswer = parser.parse_args(answer)
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
        if not Utils.utils.istestable(warnings):
            return
        msg = "\n\ndata=%s,\nerranswer=%s,\nwarnings=%s,\n\n" % (
            data,
            erranswer,
            warnings,
        )
        self.assertEqual(erranswer, warnings, msg=msg)


if __name__ == "__main__":
    unittest.main()

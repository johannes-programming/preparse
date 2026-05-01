import enum
import math
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import *

from preparse.core.PreParser import PreParser

__all__ = ["TestDataToml"]


class Utils(enum.Enum):

    utils = None

    @cached_property
    def data(self: Self) -> dict[str, Any]:
        data: dict[str, Any]
        text: str
        text = resources.read_text("preparse.tests", "data.toml")
        data = tomllib.loads(text)
        return data


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        name: str
        kwargs: dict
        kwargs_: dict
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                kwargs_ = self.convert(**kwargs)
                self.parse(**kwargs_)

    def convert(self: Self, **kwargs: Any) -> dict:
        ans: dict
        x: str
        y: Any
        ans = dict()
        for x, y in kwargs.items():
            if type(y) is float and math.isnan(y):
                ans[x] = None
            else:
                ans[x] = y
        return ans

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        answer: list
        capture: list
        data: dict
        erranswer: list
        msg: str
        superanswer: list
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
        msg = "\n\ndata=%s,\nanswer=%s,\nsolution=%s,\n\n" % (data, answer, solution)
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

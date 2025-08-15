import math
import tomllib
import unittest
from importlib import resources
from typing import *

from preparse.core import *

# Read URL of the Real Python feed from config file


class TestDataToml(unittest.TestCase):

    def get_data(self: Self) -> dict:
        text: str = resources.read_text("preparse.tests", "data.toml")
        data: dict = tomllib.loads(text)
        return data

    def test_0(self: Self) -> None:
        data: dict = self.get_data()
        data = data["data"]
        for kwargs in data:
            self.parse(**kwargs)

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        capture: list = list()

        def warn(value: Any) -> None:
            capture.append(str(value))

        parser = PreParser(warn=warn, **kwargs)
        msg: str = "parser=%r, query=%r" % (parser, query)
        answer = parser.parse_args(query)
        erranswer: list = list(capture)
        capture.clear()
        superanswer = parser.parse_args(answer)
        supererranswer: list = list(capture)
        capture.clear()
        self.assertEqual(answer, superanswer, msg=msg)
        # self.assertEqual(erranswer, supererranswer, msg=msg)
        self.assertEqual(answer, solution, msg=msg)
        if not math.isnan(warnings):
            self.assertEqual(erranswer, warnings, msg=msg)

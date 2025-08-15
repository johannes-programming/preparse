import tomllib
import unittest
from importlib import resources

from preparse.core import *
from typing import *
import math

# Read URL of the Real Python feed from config file


class TestDataToml(unittest.TestCase):

    def get_data(self:Self)->dict:
        text: str = resources.read_text("preparse.tests", "data.toml")
        data: dict = tomllib.loads(text)
        return data

    def test_0(self:Self)->None:
        data: dict = self.get_data()
        data = data["data"]
        for kwargs in data:
            self.parse(**kwargs)

    def parse(
        self:Self,
        *,
        query:Any,
        solution:Any,
        warnings:Any,
        **kwargs:Any,
    )->None:
        capture:list[str] = list()
        def warn(warning:Any)->None:
            capture.append(str(warning))
        parser = PreParser(warn=warn, **kwargs)
        answer = parser.parse_args(query)
        errlines:list=list(capture)
        capture.clear()
        superanswer = parser.parse_args(answer)
        supererrlines:list=list(capture)
        capture.clear()
        msg: str = "parser=%r, query=%r" % (parser, query)
        self.assertEqual(answer, solution, msg=msg)
        if not math.isnan(warnings):
            self.assertEqual(errlines, warnings, msg=msg)
        self.assertEqual(answer, superanswer, msg=msg)
        self.assertEqual(errlines, supererrlines, msg=msg)

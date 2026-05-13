import unittest
from typing import *

import namings

from preparse.core.Click import Click
from preparse.core.PreParser import PreParser

__all__ = ["TestPreparse"]


class TestPreParser(unittest.TestCase):

    def test_preparser_click_decorator(self: Self) -> None:
        click_decorator: Click
        parser: PreParser
        parser = PreParser()
        click_decorator = parser.click()
        self.assertIsInstance(click_decorator, Click)
        self.assertTrue(click_decorator.cmd)
        self.assertTrue(click_decorator.ctx)
        self.assertEqual(click_decorator.parser, parser)

    def test_preparser_copy(self: Self) -> None:
        parser: PreParser
        parser_copy: PreParser
        parser = PreParser()
        parser_copy = parser.copy()
        self.assertEqual(parser.optNaming, parser_copy.optNaming)

    def test_preparser_toNaming(self: Self) -> None:
        expected_keys: list[str]
        key: str
        parser: PreParser
        result: namings.Naming
        parser = PreParser()
        result = parser.toNaming()
        expected_keys = [
            "optNaming",
            "prog",
        ]
        for key in expected_keys:
            self.assertIn(key, result.keys())


if __name__ == "__main__":
    unittest.main()

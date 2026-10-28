__all__: list[str] = ["TestPreParser"]

import unittest
from typing import Any, Self

from preparse.core.Click import Click
from preparse.core.PreParser import PreParser
from preparse.enums.Nargs import Nargs


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
        self.assertEqual(parser.optdict, parser_copy.optdict)

    def test_no_options_idempotent(self: Self) -> None:
        args: list[str]
        parser: PreParser
        parser = PreParser(
            allowslong=False, allowsshort=False, expectsposix=True
        )
        args = ["-c2", "--", "-a"]
        self.assertEqual(parser.parse_args(args), args)
        self.assertEqual(parser.parse_args(parser.parse_args(args)), args)

    def test_minimize_short_bundle_with_hyphen_option(self: Self) -> None:
        parser: PreParser
        parser = PreParser(
            allowslong=False,
            bundling=0,
            optdict={"--": 2},  # type: ignore[arg-type]
        )
        self.assertEqual(parser.parse_args(["--x"]), ["--x"])

    def test_preparser_todict(self: Self) -> None:
        expected_keys: list[Any]
        parser: PreParser
        result: Any
        parser = PreParser()
        result = parser.todict()
        expected_keys = [
            "optdict",
            "prog",
        ]
        self.assertTrue(all(key in result for key in expected_keys))


if __name__ == "__main__":
    unittest.main()

__all__: list[str] = ["TestPreParser"]

import unittest
from typing import Any, Self

from preparse.core.PreParser import PreParser


class TestPreParser(unittest.TestCase):
    def test_preparser_copy(self: Self) -> None:
        parser = PreParser(shortsopts="a:", longopts=("flag",))
        parser_copy = parser.copy()
        self.assertEqual(parser.shortsopts, parser_copy.shortsopts)
        self.assertEqual(parser.longopts, parser_copy.longopts)

    def test_no_options_idempotent(self: Self) -> None:
        parser = PreParser(shortsopts=None, longopts=None, expectsposix=True)
        args = ["-c2", "--", "-a"]
        preparsed, messages = parser.parse_args(args)
        self.assertEqual(args, preparsed)
        self.assertEqual(args, parser.parse_args(preparsed)[0])

    def test_minimize_short_bundle_with_hyphen_option(self: Self) -> None:
        parser = PreParser(longopts=None, shortsopts="-::", bundling=0)
        preparsed, messages = parser.parse_args(["--x"])
        self.assertEqual(preparsed, ["--x"])

    def test_preparser_todict(self: Self) -> None:
        parser = PreParser()
        result = parser.todict()
        expected_keys = ["shortsopts", "longopts", "prog"]
        self.assertTrue(all(key in result for key in expected_keys))


if __name__ == "__main__":
    unittest.main()

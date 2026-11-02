__all__: list[str] = ["TestPreParser"]

import unittest
from typing import Any, Self

from preparse.core.PreParser import PreParser


class TestPreParser(unittest.TestCase):

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
        preparsed, messages = parser.parse_args(args)
        self.assertEqual(args, preparsed)
        self.assertEqual(args, parser.parse_args(preparsed)[0])

    def test_minimize_short_bundle_with_hyphen_option(self: Self) -> None:
        parser: PreParser
        parser = PreParser(
            allowslong=False,
            bundling=0,
            optdict={"--": 2},
        )
        preparsed, messages = parser.parse_args(["--x"])
        self.assertEqual(preparsed, ["--x"])

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

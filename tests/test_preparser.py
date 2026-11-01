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
        self.assertEqual(parser.optList, parser_copy.optList)

    def test_no_options_idempotent(self: Self) -> None:
        args: list[str]
        parser: PreParser
        parser = PreParser()
        parser.framework.allows_long = False
        parser.framework.allows_short = False
        parser.framework.is_posix = True
        args = ["-c2", "--", "-a"]
        preparsed, messages = parser.parse_args(args)
        self.assertEqual(preparsed, args)
        self.assertEqual(parser.parse_args(preparsed), args)

    def test_minimize_short_bundle_with_hyphen_option(self: Self) -> None:
        parser: PreParser
        parser = PreParser()
        parser.framework.allows_long = False
        parser.transformation.bundling = 0
        parser.optList = {"--": 2}.items()
        self.assertEqual(parser.parse_args(["--x"]), ["--x"])


if __name__ == "__main__":
    unittest.main()

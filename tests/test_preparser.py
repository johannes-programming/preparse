__all__: list[str] = ["TestPreParser"]

import unittest
from typing import Any, Self

from preparse.core.PreParser import PreParser


class TestPreParser(unittest.TestCase):
    def test_preparser_copy(self: Self) -> None:
        parser: Any
        parser_copy: Any
        parser = PreParser(shortopts="a:", longopts=("flag",))
        parser_copy = parser.copy()
        self.assertEqual(parser.shortopts, parser_copy.shortopts)
        self.assertEqual(parser.longopts, parser_copy.longopts)

    def test_no_options_idempotent(self: Self) -> None:
        args: Any
        messages: Any
        parser: Any
        preparsed: Any
        parser = PreParser(shortopts=None, longopts=None, is_posix=True)
        args = ["-c2", "--", "-a"]
        preparsed, messages = parser.parse_args(args)
        self.assertEqual(args, preparsed)
        self.assertEqual(args, parser.parse_args(preparsed)[0])

    def test_minimize_short_bundle_with_hyphen_option(self: Self) -> None:
        messages: Any
        parser: Any
        preparsed: Any
        parser = PreParser(longopts=None, shortopts="-::", bundling=0)
        preparsed, messages = parser.parse_args(["--x"])
        self.assertEqual(preparsed, ["--x"])


if __name__ == "__main__":
    unittest.main()

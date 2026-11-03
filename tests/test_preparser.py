"""Tests for the public getopt-style PreParser interface."""

import unittest

from preparse import PreParser


class TestPreParser(unittest.TestCase):
    def test_copy(self) -> None:
        parser = PreParser(shortsopts="ab:c::", longopts=("flag", "value=", "maybe=="))
        duplicate = parser.copy()
        self.assertEqual(parser, duplicate)
        self.assertIsNot(parser, duplicate)
        duplicate.shortsopts = "x"
        self.assertEqual(parser.shortsopts, "ab:c::")

    def test_no_options_idempotent(self) -> None:
        parser = PreParser(shortsopts=None, longopts=None, expectsposix=True)
        args = ["-c2", "--", "-a"]
        preparsed, messages = parser.parse_args(args)
        self.assertEqual(preparsed, args)
        self.assertEqual(messages, [])
        self.assertEqual(args, parser.parse_args(preparsed)[0])

    def test_minimize_short_bundle_with_hyphen_option(self) -> None:
        parser = PreParser(longopts=None, bundling=0, shortsopts="-::")
        self.assertEqual(parser.parse_args(["--x"])[0], ["--x"])

    def test_todict(self) -> None:
        result = PreParser().todict()
        self.assertEqual(result["shortsopts"], "")
        self.assertEqual(result["longopts"], ())
        self.assertNotIn("optdict", result)
        self.assertNotIn("allowslong", result)
        self.assertNotIn("allowsshort", result)

    def test_getopt_required_and_optional_args(self) -> None:
        parser = PreParser(shortsopts="ab:c::", longopts=("flag", "required=", "optional=="))
        args = ["-abvalue", "-c", "--flag", "--required", "value", "--optional=maybe"]
        self.assertEqual(parser.parse_args(args), (args, []))
        self.assertEqual(parser.parse_args(["-b"])[1][0].option, "b")
        self.assertEqual(parser.parse_args(["--required"])[1][0].option, "--required")

    def test_getopt_unique_abbreviation(self) -> None:
        parser = PreParser(longopts=("verbose", "version"))
        self.assertEqual(parser.parse_args(["--verb"]), (["--verbose"], []))
        self.assertEqual(len(parser.parse_args(["--ver"])[1]), 1)

    def test_none_disables_only_one_syntax(self) -> None:
        short = PreParser(shortsopts="x", longopts=None)
        long = PreParser(shortsopts=None, longopts=("alpha",))
        self.assertEqual(short.parse_args(["-x"]), (["-x"], []))
        self.assertEqual(long.parse_args(["--alpha"]), (["--alpha"], []))

    def test_validation(self) -> None:
        with self.assertRaises(TypeError):
            PreParser(shortsopts=123)
        with self.assertRaises(TypeError):
            PreParser(longopts=("okay", 123))


if __name__ == "__main__":
    unittest.main()

"""Tests for interpretation of the two option specification fields."""

import getopt
import unittest
from preparse._option_spec import option_modes
from preparse import PreParser


class GetoptSpecificationTests(unittest.TestCase):
    def test_modes(self):
        self.assertEqual(option_modes("ab:c::", ("flag", "file=", "maybe==")), {
            "-a": 0, "-b": 1, "-c": 2, "--flag": 0, "--file": 1, "--maybe": 2,
        })

    def test_getopt_compatibility_for_standard_specs(self):
        shortsopts = "ab:c"
        longopts = ("flag", "file=")
        parser = PreParser(shortsopts=shortsopts, longopts=longopts)
        examples = [
            ["-a", "-b", "value", "--flag", "--file=data"],
            ["-abx", "--fi", "file"],
            ["-c", "--flag", "-b=1"],
        ]
        for args in examples:
            with self.subTest(args=args):
                options, rest = getopt.gnu_getopt(args, shortsopts, list(longopts))
                self.assertEqual(parser.parse_args(args)[1], [])
                self.assertEqual(rest, [])
                self.assertEqual(len(options), 4 if args[0] == "-a" else 3)

    def test_unknown_short_does_not_consume_following_value(self):
        preparsed, warnings = PreParser(shortsopts="a:", longopts=()).parse_args(["-xa", "text"])
        self.assertEqual(preparsed, ["-xa", "text"])
        self.assertEqual([w.option for w in warnings], ["x"])

    def test_optional_arguments_are_attached_only(self):
        parser = PreParser(shortsopts="o::", longopts=("maybe==",), reconcilesorders=False)
        args = ["-o", "separate", "--maybe", "separate"]
        self.assertEqual(parser.parse_args(args), (args, []))

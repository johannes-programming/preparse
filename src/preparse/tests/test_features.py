import unittest

from preparse import Abbrev, Click, Nargs, PreParser


class TestPreparse(unittest.TestCase):

    def test_abbrev_enum(self):
        self.assertEqual(Abbrev.REJECT, 0)
        self.assertEqual(Abbrev.COMPLETE, 1)
        self.assertEqual(Abbrev.KEEP, 2)

    def test_nargs_enum(self):
        self.assertEqual(Nargs.NO_ARGUMENT, 0)
        self.assertEqual(Nargs.REQUIRED_ARGUMENT, 1)
        self.assertEqual(Nargs.OPTIONAL_ARGUMENT, 2)

    def test_preparser_copy(self):
        parser = PreParser()
        parser_copy = parser.copy()
        self.assertEqual(parser.abbrev, parser_copy.abbrev)
        self.assertEqual(parser.permutate, parser_copy.permutate)
        self.assertEqual(parser.posix, parser_copy.posix)
        self.assertEqual(parser.optdict, parser_copy.optdict)

    def test_preparser_parse_args(self):
        parser = PreParser()
        mock_args = ["--option", "value"]
        result = parser.parse_args(mock_args)
        self.assertEqual(result, mock_args)

    def test_preparser_todict(self):
        parser = PreParser()
        result = parser.todict()
        expected_keys = ["abbrev", "optdict", "permutate", "posix", "prog"]
        self.assertTrue(all(key in result for key in expected_keys))

    def test_preparser_click_decorator(self):
        parser = PreParser()
        click_decorator = parser.click()
        self.assertIsInstance(click_decorator, Click)
        self.assertTrue(click_decorator.cmd)
        self.assertTrue(click_decorator.ctx)
        self.assertEqual(click_decorator.parser, parser)


if __name__ == "__main__":
    unittest.main()

import unittest

from preparse.core import *


class TestPreParserCustomWarnings(unittest.TestCase):

    def test_custom_unrecognized_option_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--foo": 1, "--bar": 1, "-x": 0}
        query = ["--unknown", "value", "--foo", "bar"]

        def replacementFunction(option):
            self.assertEqual(option, "--unknown")

        parser.warnAboutUnrecognizedOption = replacementFunction
        parser.parse_args(query)

    def test_custom_invalid_option_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--foo": 1, "--bar": 1, "-x": 0}
        query = ["-z", "--foo", "value"]

        def replacementFunction(option):
            self.assertEqual(option, "z")  # Only the letter is passed in this case

        parser.warnAboutInvalidOption = replacementFunction
        parser.parse_args(query)

    def test_custom_ambiguous_option_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--foo": 1, "--foobar": 1, "--foxtrot": 1}
        query = ["--fo"]

        def replacementFunction(option, possibilities):
            self.assertEqual(option, "--fo")
            self.assertListEqual(
                list(possibilities), ["--foo", "--foobar", "--foxtrot"]
            )

        parser.warnAboutAmbiguousOption = replacementFunction
        parser.parse_args(query)

    def test_custom_unallowed_argument_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--flag": 0, "-x": 0}
        query = ["--flag=value", "-x"]

        def replacementFunction(option):
            self.assertEqual(option, "--flag")

        parser.warnAboutUnallowedArgument = replacementFunction
        parser.parse_args(query)

    def test_custom_required_argument_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--foo": 1, "--bar": 0}
        query = ["--foo"]

        def replacementFunction(option):
            self.assertEqual(option, "--foo")

        parser.warnAboutRequiredArgument = replacementFunction
        parser.parse_args(query)


if __name__ == "__main__":
    unittest.main()

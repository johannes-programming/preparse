import unittest

from preparse.core import PreParser


class TestPreParserCustomWarnings(unittest.TestCase):

    def test_custom_unrecognized_option_handler(self):
        parser = PreParser(posix=False)
        parser.optdict = {"--foo": 1, "--bar": 1, "-x": 0}
        query = ["--unknown", "value", "--foo", "bar"]

        def replacementFunction(option) -> None:
            self.assertEqual(option, "--unknown")

        parser.warnAboutUnrecognizedOption = replacementFunction
        parser.parse_args(query)


if __name__ == "__main__":
    unittest.main()

import unittest
import warnings
from preparse.core import PreParser

class TestPreParserWarnings(unittest.TestCase):

    def setUp(self):
        self.parser = PreParser(posix=False, optdict={})

    def test_warn_about_unrecognized_option(self):
        with self.assertWarns(UserWarning) as warn:
            self.parser.warnAboutUnrecognizedOption("--unknown")
        self.assertIn("unrecognized option '--unknown'", str(warn.warning))

    def test_warn_about_invalid_option(self):
        with self.assertWarns(UserWarning) as warn:
            self.parser.warnAboutInvalidOption("--invalid")
        self.assertIn("invalid option -- '--invalid'", str(warn.warning))

    def test_warn_about_ambiguous_option(self):
        with self.assertWarns(UserWarning) as warn:
            self.parser.warnAboutAmbiguousOption("--amb", ["--amber", "--ambush"])
        self.assertIn("option '--amb' is ambiguous; possibilities: '--amber' '--ambush'", str(warn.warning))

    def test_warn_about_unallowed_argument(self):
        with self.assertWarns(UserWarning) as warn:
            self.parser.warnAboutUnallowedArgument("--flag")
        self.assertIn("option '--flag' doesn't allow an argument", str(warn.warning))

    def test_warn_about_required_argument(self):
        with self.assertWarns(UserWarning) as warn:
            self.parser.warnAboutRequiredArgument("--requires")
        self.assertIn("option requires an argument -- '--requires'", str(warn.warning))

if __name__ == "__main__":
    unittest.main()

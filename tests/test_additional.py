from __future__ import annotations

__all__: list[str] = [
    "ArgumentInputTests",
    "ConfigurationTests",
    "OptdictAndCopyTests",
    "WarningTests",
]

import os
import sys
import unittest
from collections.abc import Iterator
from typing import Any, Self
from unittest.mock import patch

from preparse.abc.Message import Message
from preparse.core.Optdict import Optdict
from preparse.core.PreParser import PreParser
from preparse.enums.Nargs import Nargs
from preparse.enums.Tuning import Tuning
from preparse.messaging.AmbiguousOptionMessage import AmbiguousOptionMessage
from preparse.messaging.InvalidOptionMessage import InvalidOptionMessage
from preparse.messaging.RequiredArgumentMessage import RequiredArgumentMessage
from preparse.messaging.UnallowedArgumentMessage import (
    UnallowedArgumentMessage,
)


class WarningTests(unittest.TestCase):
    def parser_with_warnings(self: Self, **settings: Any) -> PreParser:

        return PreParser(prog="example", **settings)

    def test_long_and_short_invalid_options(self: Self, /) -> None:
        parser: PreParser
        warnings: list[Any]
        parser = self.parser_with_warnings(optdict={"--good": 0})
        preparsed, warnings = parser.parse_args(["--unknown", "-z"])
        self.assertEqual(preparsed, ["--unknown", "-z"])
        self.assertEqual(len(warnings), 2)
        self.assertTrue(
            all(isinstance(w, InvalidOptionMessage) for w in warnings)
        )
        self.assertEqual(
            (warnings[0].option, warnings[0].islong), ("--unknown", True)
        )
        self.assertEqual(
            (warnings[1].option, warnings[1].islong), ("z", False)
        )
        self.assertEqual(
            str(warnings[0]), "example: unrecognized option '--unknown'"
        )
        self.assertEqual(str(warnings[1]), "example: invalid option -- 'z'")

    def test_each_unknown_short_option_triggers_callback(
        self: Self, /
    ) -> None:
        parser: PreParser
        warnings: list[Any]
        parser = self.parser_with_warnings()
        preparsed, warnings = parser.parse_args(["-xy"])
        self.assertEqual(preparsed, ["-xy"])
        self.assertEqual([w.option for w in warnings], ["x", "y"])
        self.assertTrue(all(not w.islong for w in warnings))

    def test_ambiguous_abbreviation_reports_candidates(self: Self, /) -> None:
        parser: PreParser
        warning: AmbiguousOptionMessage
        warnings: list[Any]
        parser = self.parser_with_warnings(
            optdict={"--alpha": 0, "--alpine": 0}
        )
        preparsed, warnings = parser.parse_args(["--al"])
        self.assertEqual(preparsed, ["--al"])
        self.assertEqual(len(warnings), 1)
        warning = warnings[0]
        self.assertIsInstance(warning, AmbiguousOptionMessage)
        self.assertEqual(warning.option, "--al")
        self.assertEqual(warning.possibilities, ("--alpha", "--alpine"))
        self.assertEqual(warning.prog, "example")
        self.assertEqual(
            str(warning),
            "example: option '--al' is ambiguous; possibilities:"
            " '--alpha' '--alpine'",
        )

    def test_missing_value_for_long_and_short_options(self: Self, /) -> None:
        args: list[str]
        islong: bool
        message: str
        option: str
        parser: PreParser
        warnings: list[Any]
        for args, option, islong, message in (
            (
                ["--output"],
                "--output",
                True,
                "example: option '--output' requires an argument",
            ),
            (
                ["-o"],
                "o",
                False,
                "example: option requires an argument -- 'o'",
            ),
        ):
            with self.subTest(args=args):
                parser = self.parser_with_warnings(
                    optdict={"--output": 1, "-o": 1}
                )
                preparsed, warnings = parser.parse_args(args)
                self.assertEqual(preparsed, args)
                self.assertEqual(len(warnings), 1)
                self.assertIsInstance(warnings[0], RequiredArgumentMessage)
                self.assertEqual(
                    (warnings[0].option, warnings[0].islong), (option, islong)
                )
                self.assertEqual(str(warnings[0]), message)

    def test_value_on_flag_is_not_silently_accepted(self: Self, /) -> None:
        parser: PreParser
        warnings: list[Any]
        parser = self.parser_with_warnings(optdict={"--flag": 0})
        preparsed, warnings = parser.parse_args(["--flag=on"])
        self.assertEqual(preparsed, ["--flag=on"])
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], UnallowedArgumentMessage)
        self.assertEqual(warnings[0].option, "--flag")
        self.assertEqual(
            str(warnings[0]),
            "example: option '--flag' doesn't allow an argument",
        )

    def test_valid_options_do_not_emit_warnings(self: Self, /) -> None:
        args: list[str]
        parser: PreParser
        warnings: list[Any]
        parser = self.parser_with_warnings(
            optdict={"--flag": 0, "--output": 1, "--maybe": 2}
        )
        args = ["--flag", "--output", "file", "--maybe=auto"]
        preparsed, warnings = parser.parse_args(args)
        self.assertEqual(preparsed, args)
        self.assertEqual(warnings, [])

    def test_callback_can_turn_a_warning_into_an_exception(
        self: Self, /
    ) -> None:
        parser: PreParser
        parser = PreParser(prog="strict")
        preparsed, messages = parser.parse_args(["--unknown"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].prog, "strict")
        self.assertEqual(messages[0].option, "--unknown")

    def test_warning_object_copy_dict_repr_and_mutable_attributes(
        self: Self, /
    ) -> None:
        duplicate: Message
        examples: list[Message]
        original: Message
        examples = [
            InvalidOptionMessage(prog="tool", option="-x", islong=False),
            RequiredArgumentMessage(prog="tool", option="--out", islong=True),
            UnallowedArgumentMessage(prog="tool", option="--flag"),
            AmbiguousOptionMessage(
                prog="tool", option="--fo", possibilities=["--foo", "--force"]
            ),
        ]
        for original in examples:
            with self.subTest(warning=type(original).__name__):
                self.assertIsInstance(original, Message)
                self.assertEqual(
                    original.todict()["prog"], "tool", msg=str(type(original))
                )
                self.assertIn(original.getmsg(), str(original))
                self.assertIn(type(original).__name__, repr(original))
                self.assertIn(original.option, repr(original))
                duplicate = original.copy()
                self.assertIs(type(duplicate), type(original))
                self.assertIsNot(duplicate, original)
                self.assertEqual(duplicate.todict(), original.todict())
                duplicate.option = "--changed"
                duplicate.prog = 100
                self.assertNotEqual(duplicate.todict(), original.todict())
                self.assertEqual(original.prog, "tool")
                self.assertEqual(duplicate.prog, "100")

    def test_warning_data_is_defensively_copied(self: Self, /) -> None:
        exported: dict[str, Any]
        warning: AmbiguousOptionMessage
        warning = AmbiguousOptionMessage(
            prog="tool", option="--a", possibilities=["--abc"]
        )
        exported = warning.todict()
        exported["option"] = "not-the-warning"
        self.assertEqual(warning.option, "--a")
        warning.possibilities = (123, "--abd")
        self.assertEqual(warning.possibilities, ("123", "--abd"))


class ArgumentInputTests(unittest.TestCase):
    def test_empty_list_and_tuple(self: Self, /) -> None:
        parser: PreParser
        parser = PreParser()
        preparsed, messages = parser.parse_args([])
        self.assertEqual(preparsed, [])
        preparsed, messages = parser.parse_args(())
        self.assertEqual(preparsed, [])
        preparsed, messages = parser.parse_args(("text", "more"))
        self.assertEqual(preparsed, ["text", "more"])

    def test_generator_is_consumed_once(self: Self, /) -> None:
        consumed: list[Any]
        parser: PreParser
        parser = PreParser(optdict={"--flag": 0})
        consumed = []

        def generated() -> Iterator[str]:
            item: str
            for item in ("--flag", "file"):
                consumed.append(item)
                yield item

        preparsed, messages = parser.parse_args(generated())
        self.assertEqual(preparsed, ["--flag", "file"])
        self.assertEqual(consumed, ["--flag", "file"])

    def test_none_uses_sys_argv_and_prog_uses_basename(self: Self, /) -> None:
        parser: PreParser
        with patch.object(sys, "argv", ["/tmp/mytool.py", "--flag", "tail"]):
            parser = PreParser(optdict={"--flag": 0})
            self.assertEqual(parser.prog, "mytool.py")
            preparsed, messages = parser.parse_args(None)
            self.assertEqual(preparsed, ["--flag", "tail"])
            preparsed, messages = parser.parse_args()
            self.assertEqual(preparsed, ["--flag", "tail"])
            preparsed, messages = parser.parse_args([])
            self.assertEqual(preparsed, [])

    def test_nonstring_arguments_are_converted_to_strings(
        self: Self, /
    ) -> None:
        parser: PreParser
        parser = PreParser(allowslong=False, allowsshort=False)
        preparsed, messages = parser.parse_args([7, None, True, "-z"])
        self.assertEqual(
            preparsed,
            ["7", "None", "True", "-z"],
        )
        parser = PreParser(optdict={"--number": 1})
        preparsed, messages = parser.parse_args(["--number", 42])
        self.assertEqual(preparsed, ["--number", "42"])


class ConfigurationTests(unittest.TestCase):
    def test_posix_inference_respects_environment_variable_presence(
        self: Self, /
    ) -> None:
        parser: PreParser
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(PreParser(expectsposix="infer").expectsposix)
        with patch.dict(os.environ, {"POSIXLY_CORRECT": ""}, clear=True):
            self.assertTrue(PreParser(expectsposix="infer").expectsposix)
        with patch.dict(os.environ, {"POSIXLY_CORRECT": "0"}, clear=True):
            self.assertTrue(PreParser(expectsposix="infer").expectsposix)
        parser = PreParser(expectsposix=False)
        with patch.dict(os.environ, {"POSIXLY_CORRECT": "1"}, clear=True):
            parser.expectsposix = "infer"
        self.assertTrue(parser.expectsposix)

    def test_abbreviation_expansion_and_recognition_are_independent(
        self: Self, /
    ) -> None:
        expands: bool
        expects: bool
        output: list[str]
        parser: PreParser
        reported: list[Any]
        warning_type: type[Message] | None
        for expands, expects, output, warning_type in (
            (True, True, ["--verbose"], None),
            (False, True, ["--ver"], None),
            (True, False, ["--ver"], InvalidOptionMessage),
            (False, False, ["--ver"], InvalidOptionMessage),
        ):
            with self.subTest(expands=expands, expects=expects):
                reported = []

                parser = PreParser(
                    optdict={"--verbose": 0},
                    expandsabbr=expands,
                    expectsabbr=expects,
                )
                preparsed, reported = parser.parse_args(["--ver"])
                self.assertEqual(preparsed, output)
                self.assertEqual(len(reported), int(warning_type is not None))
                if warning_type is not None:
                    self.assertIsInstance(reported[0], warning_type)

    def test_no_option_syntax_is_truly_positional_only(self: Self, /) -> None:
        args: list[str]
        parser: PreParser
        recorded: list[Message]
        parser = PreParser(
            allowslong=False,
            allowsshort=False,
            expectsposix=True,
            reconcilesorders=True,
        )
        args = ["--unrecognized", "-x", "--", "file"]
        preparsed, recorded = parser.parse_args(args)
        self.assertEqual(preparsed, args)
        self.assertEqual(recorded, [])

    def test_disabling_long_options_preserves_short_bundle_interpretation(
        self: Self,
        /,
    ) -> None:
        parser: PreParser
        recorded: list[Any]
        parser = PreParser(
            allowslong=False,
            allowsshort=True,
            optdict={"--": 0, "-x": 1},
        )
        preparsed, recorded = parser.parse_args(["--x", "value"])
        self.assertEqual(preparsed, ["--x", "value"])
        self.assertEqual(recorded, [])

    def test_posix_ordering_and_reconciliation_combinations(
        self: Self, /
    ) -> None:
        cases: tuple[Any, ...]
        expected: Any
        parser: PreParser
        posix: bool
        reconcile: bool
        cases = (
            (False, True, ["--flag", "file", "tail"]),
            (True, False, ["file", "--flag", "tail"]),
            (True, True, ["--", "file", "--flag", "tail"]),
        )
        for posix, reconcile, expected in cases:
            with self.subTest(posix=posix, reconcilesorders=reconcile):
                parser = PreParser(
                    optdict={"--flag": 0},
                    expectsposix=posix,
                    reconcilesorders=reconcile,
                )
                preparsed, messages = parser.parse_args(
                    ["file", "--flag", "tail"]
                )
                self.assertEqual(preparsed, expected)

    def test_special_minimize_and_maximize_with_long_options(
        self: Self, /
    ) -> None:
        args: list[str]
        cases: tuple[Any, ...]
        expected: Any
        parser: PreParser
        tuning: Tuning
        cases = (
            (Tuning.MINIMIZE, ["--flag", "--", "file"], ["--flag", "file"]),
            (Tuning.MINIMIZE, ["--flag", "--", "-x"], ["--flag", "--", "-x"]),
            (Tuning.MAXIMIZE, ["--flag", "file"], ["--flag", "--", "file"]),
            (
                Tuning.MAXIMIZE,
                ["--flag", "--", "file"],
                ["--flag", "--", "file"],
            ),
        )
        for tuning, args, expected in cases:
            with self.subTest(tuning=tuning, args=args):
                parser = PreParser(optdict={"--flag": 0}, special=tuning)
                preparsed, messages = parser.parse_args(args)
                self.assertEqual(preparsed, expected)

    def test_bundling_modes_with_a_long_option(self: Self, /) -> None:
        args: list[str]
        expected: Any
        parser: PreParser
        tuning: Tuning
        for tuning, args, expected in (
            (Tuning.MINIMIZE, ["-ab", "--flag"], ["-a", "-b", "--flag"]),
            (Tuning.MAXIMIZE, ["-a", "-b", "--flag"], ["-ab", "--flag"]),
        ):
            with self.subTest(tuning=tuning):
                parser = PreParser(
                    optdict={"-a": 0, "-b": 0, "--flag": 0},
                    bundling=tuning,
                )
                preparsed, messages = parser.parse_args(args)
                self.assertEqual(preparsed, expected)


class OptdictAndCopyTests(unittest.TestCase):
    def test_optdict_coerces_keys_and_falls_back_on_noninteger_values(
        self: Self, /
    ) -> None:
        name: str
        options: Optdict
        options = Optdict(
            {
                5: 0,
                "--required": 1,
                "--unknown": 999,
                "--none": None,
                "--string": None,
            }
        )
        self.assertEqual(options["5"], Nargs.NO_ARGUMENT)
        self.assertEqual(options["--required"], Nargs.REQUIRED_ARGUMENT)
        for name in ("--unknown", "--none", "--string"):
            self.assertEqual(options[name], Nargs.OPTIONAL_ARGUMENT)
        self.assertEqual(tuple(options.keys()), tuple(sorted(options.keys())))

    def test_optdict_accepts_iterables_and_its_copy_is_independent(
        self: Self, /
    ) -> None:
        copy: Optdict
        original: Optdict
        original = Optdict([("--flag", 0), (17, 1)])
        copy = original.copy()
        self.assertIsNot(original, copy)
        self.assertEqual(dict(original.items()), dict(copy.items()))
        copy.update({"--extra": 2})
        self.assertNotIn("--extra", original)
        self.assertEqual(copy["--extra"], Nargs.OPTIONAL_ARGUMENT)

    def test_setting_parser_optdict_replaces_contents_not_reference(
        self: Self, /
    ) -> None:
        options_before: Optdict
        parser: PreParser
        parser = PreParser(optdict={"--old": 0})
        options_before = parser.optdict
        parser.optdict = {"--new": 1, 99: 0}
        self.assertIs(parser.optdict, options_before)
        self.assertNotIn("--old", parser.optdict)
        self.assertEqual(parser.optdict["--new"], Nargs.REQUIRED_ARGUMENT)
        self.assertEqual(parser.optdict["99"], Nargs.NO_ARGUMENT)
        parser.optdict.clear()
        self.assertEqual(dict(parser.optdict.items()), {})

    def test_copy_carries_all_config_and_is_independent(self: Self, /) -> None:
        attr: str
        copy: PreParser
        original: PreParser

        original = PreParser(
            allowslong=False,
            allowsshort=True,
            bundling=Tuning.MINIMIZE,
            expandsabbr=False,
            expectsabbr=False,
            expectsposix=True,
            optdict={"-a": 0},
            prog="original",
            reconcilesorders=False,
            special=Tuning.MAXIMIZE,
        )
        copy = original.copy()
        self.assertIsNot(copy, original)
        self.assertIsNot(copy.optdict, original.optdict)
        for attr in (
            "allowslong",
            "allowsshort",
            "bundling",
            "expandsabbr",
            "expectsabbr",
            "expectsposix",
            "optdict",
            "prog",
            "reconcilesorders",
            "special",
        ):
            with self.subTest(attribute=attr):
                self.assertEqual(getattr(copy, attr), getattr(original, attr))
        copy.allowslong = True
        copy.optdict = {"--new": 1}
        copy.prog = "copy"
        self.assertFalse(original.allowslong)
        self.assertEqual(
            dict(original.optdict.items()), {"-a": Nargs.NO_ARGUMENT}
        )
        self.assertEqual(original.prog, "original")

    def test_construction_from_another_parser_allows_overrides(
        self: Self, /
    ) -> None:
        derived: PreParser
        original: PreParser
        original = PreParser(
            optdict={"--one": 0}, expandsabbr=True, prog="base"
        )
        derived = PreParser(
            original, expandsabbr=False, optdict={"--two": 1}, prog=123
        )
        self.assertFalse(derived.expandsabbr)
        self.assertTrue(original.expandsabbr)
        self.assertEqual(derived.prog, "123")
        self.assertEqual(original.prog, "base")
        self.assertEqual(
            dict(derived.optdict.items()), {"--two": Nargs.REQUIRED_ARGUMENT}
        )
        self.assertEqual(
            dict(original.optdict.items()), {"--one": Nargs.NO_ARGUMENT}
        )

    def test_parser_repr_and_todict_are_complete(self: Self, /) -> None:
        expected_keys: set[str]
        exported: dict[str, Any]
        parser: PreParser
        parser = PreParser(optdict={"--flag": 0}, prog="demo")
        expected_keys = {
            "allowslong",
            "allowsshort",
            "bundling",
            "expandsabbr",
            "expectsabbr",
            "expectsposix",
            "optdict",
            "prog",
            "reconcilesorders",
            "special",
        }
        exported = parser.todict()
        self.assertEqual(set(exported), expected_keys)
        self.assertEqual(exported["prog"], "demo")
        self.assertIn("PreParser", repr(parser))
        exported["prog"] = "changed"
        self.assertEqual(parser.prog, "demo")

    def test_tuning_enum_valid_values_and_missing_fallback(
        self: Self, /
    ) -> None:
        parser: PreParser
        unknown: int
        self.assertEqual(Tuning.MINIMIZE, 0)
        self.assertEqual(Tuning.MAXIMIZE, 1)
        self.assertEqual(Tuning.MAINTAIN, 2)
        for unknown in (-1, 17):
            with self.subTest(value=unknown):
                self.assertIs(Tuning(unknown), Tuning.MAINTAIN)
                self.assertIs(Nargs(unknown), Nargs.OPTIONAL_ARGUMENT)
        parser = PreParser(bundling=999, special=-1)
        self.assertIs(parser.bundling, Tuning.MAINTAIN)
        self.assertIs(parser.special, Tuning.MAINTAIN)


if __name__ == "__main__":
    unittest.main()

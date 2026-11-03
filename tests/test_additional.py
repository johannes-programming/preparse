from __future__ import annotations

__all__: list[str] = [
    "ArgumentInputTests",
    "ConfigurationTests",
    "GetoptConfigurationTests",
    "WarningTests",
]

import os
import sys
import unittest
from collections.abc import Iterator
from typing import Any, Self
from unittest.mock import patch

from preparse.abc.Message import Message
from preparse.core.PreParser import PreParser
from preparse.enum.Tuning import Tuning
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
        parser = self.parser_with_warnings(longopts=("good",))
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
        parser = self.parser_with_warnings(longopts=("alpha", "alpine"))
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
                    shortopts="o:", longopts=("output=",)
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
        parser = self.parser_with_warnings(longopts=("flag",))
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
            longopts=("flag", "maybe=?", "output=")
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
        parser = PreParser(longopts=("flag",))
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
            parser = PreParser(longopts=("flag",))
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
        parser = PreParser(longopts=None, shortopts=None)
        preparsed, messages = parser.parse_args([7, None, True, "-z"])
        self.assertEqual(
            preparsed,
            ["7", "None", "True", "-z"],
        )
        parser = PreParser(longopts=("number=",))
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
        output: list[str]
        parser: PreParser
        reported: list[Any]
        warning_type: type[Message] | None
        for expands, output, warning_type in (
            (True, ["--verbose"], None),
            (False, ["--ver"], None),
        ):
            with self.subTest(expands=expands):
                reported = []

                parser = PreParser(
                    longopts=("verbose",),
                    expandsabbr=expands,
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
            longopts=None,
            shortopts=None,
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
            longopts=None,
            shortopts="-x:",
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
                    longopts=("flag",),
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
                parser = PreParser(longopts=("flag",), special=tuning)
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
                    shortopts="ab",
                    longopts=("flag",),
                    bundling=tuning,
                )
                preparsed, messages = parser.parse_args(args)
                self.assertEqual(preparsed, expected)


class GetoptConfigurationTests(unittest.TestCase):
    def test_default_and_disabled_option_kinds(self: Self, /) -> None:
        parser = PreParser()
        self.assertEqual(parser.shortopts, "")
        self.assertEqual(parser.longopts, ())
        parser.shortopts = None
        parser.longopts = None
        self.assertEqual(
            parser.parse_args(["-a", "--flag", "--"]),
            (["-a", "--flag", "--"], []),
        )

    def test_short_and_long_argument_modes(self: Self, /) -> None:
        parser = PreParser(
            shortopts="ab:c::",
            longopts=("flag", "output=", "maybe=?"),
            prog="example",
        )
        original = [
            "-a",
            "-bfile",
            "-cdata",
            "--flag",
            "--output",
            "path",
            "--maybe=val",
        ]
        output, warnings = parser.parse_args(original)
        self.assertEqual(output, original)
        self.assertEqual(warnings, [])
        output, warnings = parser.parse_args(["-b"])
        self.assertEqual(output, ["-b"])
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], RequiredArgumentMessage)

    def test_getopt_exact_long_option_takes_precedence(self: Self, /) -> None:
        parser = PreParser(longopts=("mode=", "mode"), prog="example")
        result, warnings = parser.parse_args(["--mode"])
        self.assertEqual(result, ["--mode"])
        self.assertEqual(warnings, [])
        result, warnings = parser.parse_args(["--mo"])
        self.assertEqual(result, ["--mo"])
        self.assertIsInstance(warnings[0], AmbiguousOptionMessage)

    def test_optional_arguments_do_not_consume_following_token(
        self: Self, /
    ) -> None:
        parser = PreParser(shortopts="x::", longopts=("maybe=?",))
        result, warnings = parser.parse_args(
            ["-x", "value", "--maybe", "tail"]
        )
        self.assertEqual(result, ["-x", "--maybe", "value", "tail"])
        self.assertEqual(warnings, [])

    def test_copy_carries_all_config_and_is_independent(self: Self, /) -> None:
        original = PreParser(
            shortopts="a",
            longopts=None,
            bundling=Tuning.MINIMIZE,
            expandsabbr=False,
            expectsposix=True,
            prog="original",
            reconcilesorders=False,
            special=Tuning.MAXIMIZE,
        )
        copy = original.copy()
        self.assertIsNot(copy, original)
        self.assertEqual(copy.todict(), original.todict())
        copy.shortopts = "b:"
        copy.longopts = ("new=",)
        copy.prog = "copy"
        self.assertEqual(original.shortopts, "a")
        self.assertIsNone(original.longopts)
        self.assertEqual(original.prog, "original")

    def test_construction_from_another_parser_allows_overrides(
        self: Self, /
    ) -> None:
        original = PreParser(longopts=("one",), expandsabbr=True, prog="base")
        derived = PreParser(
            original, expandsabbr=False, longopts=("two=",), prog=123
        )
        self.assertFalse(derived.expandsabbr)
        self.assertTrue(original.expandsabbr)
        self.assertEqual(derived.prog, "123")
        self.assertEqual(original.prog, "base")
        self.assertEqual(derived.longopts, ("two=",))
        self.assertEqual(original.longopts, ("one",))

    def test_parser_repr_and_todict_are_complete(self: Self, /) -> None:
        parser = PreParser(longopts=("flag",), prog="demo")
        self.assertEqual(
            set(parser.todict()),
            {
                "shortopts",
                "longopts",
                "bundling",
                "expandsabbr",
                "expectsposix",
                "prog",
                "reconcilesorders",
                "special",
            },
        )
        self.assertEqual(parser.todict()["prog"], "demo")
        self.assertIn("PreParser", repr(parser))
        exported = parser.todict()
        exported["prog"] = "changed"
        self.assertEqual(parser.prog, "demo")

    def test_tuning_enum_valid_values_and_missing_fallback(
        self: Self, /
    ) -> None:
        self.assertEqual(Tuning.MINIMIZE, 0)
        self.assertEqual(Tuning.MAXIMIZE, 1)
        self.assertEqual(Tuning.MAINTAIN, 2)
        for unknown in (-1, 17):
            with self.subTest(value=unknown):
                self.assertIs(Tuning(unknown), Tuning.MAINTAIN)
        parser = PreParser(bundling=999, special=-1)
        self.assertIs(parser.bundling, Tuning.MAINTAIN)
        self.assertIs(parser.special, Tuning.MAINTAIN)


if __name__ == "__main__":
    unittest.main()

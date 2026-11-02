from __future__ import annotations

__all__: list[str] = [
    "ArgumentInputTests",
    "ClickIntegrationTests",
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

import click

from preparse import (
    Nargs,
    Optdict,
    PreparseAmbiguousOptionWarning,
    PreparseInvalidOptionWarning,
    PreParser,
    PreparseRequiredArgumentWarning,
    PreparseUnallowedArgumentWarning,
    PreparseWarning,
    Tuning,
)


class WarningTests(unittest.TestCase):
    def parser_with_warnings(
        self: Self, **settings: Any
    ) -> tuple[PreParser, list[Any]]:
        captured: list[Any]
        captured = []

        def capture(warning: Any) -> None:
            captured.append(warning)

        return PreParser(prog="example", warn=capture, **settings), captured

    def test_long_and_short_invalid_options(self: Self, /) -> None:
        parser: PreParser
        warnings: list[Any]
        parser, warnings = self.parser_with_warnings(optdict={"--good": 0})
        self.assertEqual(
            parser.parse_args(["--unknown", "-z"]), ["--unknown", "-z"]
        )
        self.assertEqual(len(warnings), 2)
        self.assertTrue(
            all(isinstance(w, PreparseInvalidOptionWarning) for w in warnings)
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
        parser, warnings = self.parser_with_warnings()
        self.assertEqual(parser.parse_args(["-xy"]), ["-xy"])
        self.assertEqual([w.option for w in warnings], ["x", "y"])
        self.assertTrue(all(not w.islong for w in warnings))

    def test_ambiguous_abbreviation_reports_candidates(self: Self, /) -> None:
        parser: PreParser
        warning: PreparseAmbiguousOptionWarning
        warnings: list[Any]
        parser, warnings = self.parser_with_warnings(
            optdict={"--alpha": 0, "--alpine": 0}
        )
        self.assertEqual(parser.parse_args(["--al"]), ["--al"])
        self.assertEqual(len(warnings), 1)
        warning = warnings[0]
        self.assertIsInstance(warning, PreparseAmbiguousOptionWarning)
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
                parser, warnings = self.parser_with_warnings(
                    optdict={"--output": 1, "-o": 1}
                )
                self.assertEqual(parser.parse_args(args), args)
                self.assertEqual(len(warnings), 1)
                self.assertIsInstance(
                    warnings[0], PreparseRequiredArgumentWarning
                )
                self.assertEqual(
                    (warnings[0].option, warnings[0].islong), (option, islong)
                )
                self.assertEqual(str(warnings[0]), message)

    def test_value_on_flag_is_not_silently_accepted(self: Self, /) -> None:
        parser: PreParser
        warnings: list[Any]
        parser, warnings = self.parser_with_warnings(optdict={"--flag": 0})
        self.assertEqual(parser.parse_args(["--flag=on"]), ["--flag=on"])
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], PreparseUnallowedArgumentWarning)
        self.assertEqual(warnings[0].option, "--flag")
        self.assertEqual(
            str(warnings[0]),
            "example: option '--flag' doesn't allow an argument",
        )

    def test_valid_options_do_not_emit_warnings(self: Self, /) -> None:
        args: list[str]
        parser: PreParser
        warnings: list[Any]
        parser, warnings = self.parser_with_warnings(
            optdict={"--flag": 0, "--output": 1, "--maybe": 2}
        )
        args = ["--flag", "--output", "file", "--maybe=auto"]
        self.assertEqual(parser.parse_args(args), args)
        self.assertEqual(warnings, [])

    def test_callback_can_turn_a_warning_into_an_exception(
        self: Self, /
    ) -> None:
        caught: Any
        parser: PreParser

        def reject(warning: Any) -> None:
            raise warning

        parser = PreParser(prog="strict", warn=reject)
        with self.assertRaises(PreparseInvalidOptionWarning) as caught:
            parser.parse_args(["--unknown"])
        self.assertEqual(caught.exception.prog, "strict")
        self.assertEqual(caught.exception.option, "--unknown")

    def test_warning_object_copy_dict_repr_and_mutable_attributes(
        self: Self, /
    ) -> None:
        duplicate: PreparseWarning
        examples: list[PreparseWarning]
        original: PreparseWarning
        examples = [
            PreparseInvalidOptionWarning(
                prog="tool", option="-x", islong=False
            ),
            PreparseRequiredArgumentWarning(
                prog="tool", option="--out", islong=True
            ),
            PreparseUnallowedArgumentWarning(prog="tool", option="--flag"),
            PreparseAmbiguousOptionWarning(
                prog="tool", option="--fo", possibilities=["--foo", "--force"]
            ),
        ]
        for original in examples:
            with self.subTest(warning=type(original).__name__):
                self.assertIsInstance(original, PreparseWarning)
                self.assertEqual(original.todict()["prog"], "tool")
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
        warning: PreparseAmbiguousOptionWarning
        warning = PreparseAmbiguousOptionWarning(
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
        self.assertEqual(parser.parse_args([]), [])
        self.assertEqual(parser.parse_args(()), [])
        self.assertEqual(parser.parse_args(("text", "more")), ["text", "more"])

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

        self.assertEqual(parser.parse_args(generated()), ["--flag", "file"])
        self.assertEqual(consumed, ["--flag", "file"])

    def test_none_uses_sys_argv_and_prog_uses_basename(self: Self, /) -> None:
        parser: PreParser
        with patch.object(sys, "argv", ["/tmp/mytool.py", "--flag", "tail"]):
            parser = PreParser(optdict={"--flag": 0})
            self.assertEqual(parser.prog, "mytool.py")
            self.assertEqual(parser.parse_args(None), ["--flag", "tail"])
            self.assertEqual(parser.parse_args(), ["--flag", "tail"])
            self.assertEqual(parser.parse_args([]), [])

    def test_nonstring_arguments_are_converted_to_strings(
        self: Self, /
    ) -> None:
        parser: PreParser
        parser = PreParser(allowslong=False, allowsshort=False)
        self.assertEqual(
            parser.parse_args([7, None, True, "-z"]),
            ["7", "None", "True", "-z"],
        )
        parser = PreParser(optdict={"--number": 1})
        self.assertEqual(
            parser.parse_args(["--number", 42]), ["--number", "42"]
        )


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
        warning_type: type[PreparseWarning] | None
        for expands, expects, output, warning_type in (
            (True, True, ["--verbose"], None),
            (False, True, ["--ver"], None),
            (True, False, ["--ver"], PreparseInvalidOptionWarning),
            (False, False, ["--ver"], PreparseInvalidOptionWarning),
        ):
            with self.subTest(expands=expands, expects=expects):
                reported = []

                def capture(warning: Any) -> None:
                    reported.append(warning)

                parser = PreParser(
                    optdict={"--verbose": 0},
                    expandsabbr=expands,
                    expectsabbr=expects,
                    warn=capture,
                )
                self.assertEqual(parser.parse_args(["--ver"]), output)
                self.assertEqual(len(reported), int(warning_type is not None))
                if warning_type is not None:
                    self.assertIsInstance(reported[0], warning_type)

    def test_no_option_syntax_is_truly_positional_only(self: Self, /) -> None:
        args: list[str]
        parser: PreParser
        recorded: list[PreparseWarning]
        recorded = []
        parser = PreParser(
            allowslong=False,
            allowsshort=False,
            expectsposix=True,
            reconcilesorders=True,
            warn=recorded.append,
        )
        args = ["--unrecognized", "-x", "--", "file"]
        self.assertEqual(parser.parse_args(args), args)
        self.assertEqual(recorded, [])

    def test_disabling_long_options_preserves_short_bundle_interpretation(
        self: Self,
        /,
    ) -> None:
        parser: PreParser
        recorded: list[Any]
        recorded = []
        parser = PreParser(
            allowslong=False,
            allowsshort=True,
            optdict={"--": 0, "-x": 1},
            warn=recorded.append,
        )
        self.assertEqual(parser.parse_args(["--x", "value"]), ["--x", "value"])
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
                self.assertEqual(
                    parser.parse_args(["file", "--flag", "tail"]), expected
                )

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
                self.assertEqual(parser.parse_args(args), expected)

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
                self.assertEqual(parser.parse_args(args), expected)


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
                "--string": "1",
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

        def capture(_warning: Any) -> None:
            return

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
            warn=capture,
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
        self.assertTrue(callable(copy.warn))
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
            "warn",
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


class ClickIntegrationTests(unittest.TestCase):
    def test_reflection_handles_flags_arguments_prompt_and_secondary_opts(
        self: Self, /
    ) -> None:
        command: click.Command
        expected: Any
        no_arguments: click.Option
        parser: PreParser
        prompted: click.Option
        required: click.Option
        required = click.Option(["--required", "-r"], nargs=1)
        prompted = click.Option(
            ["--prompt"], prompt="Enter value", prompt_required=False
        )
        no_arguments = click.Option(["--zero"])
        # Explicitly set these values to exercise all reflection branches,
        # regardless of Click's version-specific flag_value defaults.
        required.flag_value = None
        prompted.flag_value = None
        no_arguments.flag_value = None
        no_arguments.nargs = 0
        command = click.Command(
            "demo",
            params=[
                click.Option(["--flag", "-f"], is_flag=True),
                required,
                click.Option(
                    ["--optional"], is_flag=False, flag_value="default"
                ),
                prompted,
                no_arguments,
                click.Option(["--enabled/--disabled"]),
                click.Argument(["file"]),
            ],
        )
        parser = PreParser(optdict={"--stale": 0})
        parser.reflectClickCommand(command)
        expected = {
            "--flag": Nargs.NO_ARGUMENT,
            "-f": Nargs.NO_ARGUMENT,
            "--required": Nargs.REQUIRED_ARGUMENT,
            "-r": Nargs.REQUIRED_ARGUMENT,
            "--optional": Nargs.OPTIONAL_ARGUMENT,
            "--prompt": Nargs.OPTIONAL_ARGUMENT,
            "--zero": Nargs.NO_ARGUMENT,
            "--enabled": Nargs.NO_ARGUMENT,
            "--disabled": Nargs.NO_ARGUMENT,
        }
        self.assertEqual(dict(parser.optdict.items()), expected)
        self.assertNotIn("file", parser.optdict)
        self.assertNotIn("--stale", parser.optdict)

    def test_standalone_function_decorator_parses_and_preserves_metadata(
        self: Self, /
    ) -> None:
        command: click.Command
        context: click.Context
        parser: PreParser
        seen: list[Any]
        parser = PreParser(optdict={"--old": 0}, prog="original")
        command = click.Command("demo", params=[click.Option(["--value"])])
        context = click.Context(command, info_name="subcommand")
        seen = []

        @parser.click()
        def callback(cmd: Any, ctx: Any, args: Any) -> Any:
            """Function documentation."""
            seen.append((cmd, ctx, args))
            return args

        self.assertEqual(callback.__name__, "callback")
        self.assertEqual(callback.__doc__, "Function documentation.")
        self.assertEqual(
            callback(command, context, ["--value", "7"]), ["--value", "7"]
        )
        self.assertEqual(seen, [(command, context, ["--value", "7"])])
        self.assertEqual(parser.prog, "original")
        self.assertEqual(
            dict(parser.optdict.items()), {"--old": Nargs.NO_ARGUMENT}
        )

    def test_cmd_and_ctx_toggles_act_independently(self: Self, /) -> None:
        command: click.Command
        context: click.Context
        observed: list[Any]
        parser: PreParser
        real_parse: Any
        use_cmd: bool
        use_ctx: bool
        wrapped: Any
        command = click.Command(
            "demo", params=[click.Option(["--reflected"], is_flag=True)]
        )
        context = click.Context(command, info_name="from-context")
        for use_cmd in (False, True):
            for use_ctx in (False, True):
                with self.subTest(cmd=use_cmd, ctx=use_ctx):
                    parser = PreParser(
                        optdict={"--seed": 0}, prog="from-parser"
                    )
                    observed = []
                    real_parse = PreParser.parse_args

                    def snapshot(self: Any, args: Any = None) -> Any:
                        observed.append(
                            (dict(self.optdict.items()), self.prog)
                        )
                        return real_parse(self, args)

                    def callback(cmd: Any, ctx: Any, args: Any) -> Any:
                        return args

                    wrapped = parser.click(cmd=use_cmd, ctx=use_ctx)(callback)
                    with patch.object(PreParser, "parse_args", snapshot):
                        self.assertEqual(
                            wrapped(command, context, ["tail"]), ["tail"]
                        )
                    self.assertEqual(len(observed), 1)
                    self.assertEqual(
                        observed[0][0],
                        (
                            {"--reflected": Nargs.NO_ARGUMENT}
                            if use_cmd
                            else {"--seed": Nargs.NO_ARGUMENT}
                        ),
                    )
                    self.assertEqual(
                        observed[0][1],
                        "from-context" if use_ctx else "from-parser",
                    )
                    self.assertEqual(parser.prog, "from-parser")
                    self.assertEqual(
                        dict(parser.optdict.items()),
                        {"--seed": Nargs.NO_ARGUMENT},
                    )

    def test_bound_method_decorator(self: Self, /) -> None:
        command: click.Command
        context: click.Context
        decorated_method: Any
        parser: PreParser
        received: list[Any]
        parser = PreParser()
        received = []

        class Recorder(click.Command):
            def parse_args(self: Self, ctx: Any, args: Any) -> Any:
                received.append((self, ctx, list(args)))
                return list(args)

        command = Recorder(
            "demo", params=[click.Option(["--flag"], is_flag=True)]
        )
        context = click.Context(command, info_name="demo")
        decorated_method = parser.click()(command.parse_args)
        self.assertEqual(
            decorated_method(context, ["--flag", "file"]), ["--flag", "file"]
        )
        self.assertEqual(received, [(command, context, ["--flag", "file"])])

    def test_click_command_object_decorator(self: Self, /) -> None:
        command: click.Command
        context: click.Context
        decorated_object: Any
        parser: PreParser
        received: list[Any]
        parser = PreParser()
        received = []

        class Recorder(click.Command):
            def parse_args(self: Self, ctx: Any, args: Any) -> Any:
                received.append((self, ctx, list(args)))
                return list(args)

        command = Recorder(
            "demo", params=[click.Option(["--flag"], is_flag=True)]
        )
        decorated_object = parser.click()(command)
        self.assertIs(decorated_object, command)
        context = click.Context(command, info_name="demo")
        self.assertEqual(
            command.parse_args(context, ["--flag", "file"]), ["--flag", "file"]
        )
        self.assertEqual(received, [(command, context, ["--flag", "file"])])

    def test_context_reflection_updates_program_name(self: Self, /) -> None:
        command: click.Command
        context: click.Context
        parser: PreParser
        parser = PreParser(prog="before")
        command = click.Command("demo")
        context = click.Context(command, info_name="nested-name")
        parser.reflectClickContext(context)
        self.assertEqual(parser.prog, "nested-name")


if __name__ == "__main__":
    unittest.main()

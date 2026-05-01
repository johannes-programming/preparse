import enum
import math
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import *

import click
from click.testing import CliRunner

from preparse.core.PreParser import PreParser

__all__ = ["TestMainFunction"]


class expit:

    def function(x: float) -> float:
        p: float
        try:
            p = math.exp(-x)
        except OverflowError:
            p = float("+inf")
        return 1 / (1 + p)

    @PreParser(reconcilesorders=True, expectsPOSIX=False).click()
    @click.command(add_help_option=False)
    @click.help_option("-h", "--help")
    @click.version_option("1.2.3", "-V", "--version")
    @click.argument("x", type=float)
    def main(x: float) -> None:
        """applies the expit function to x"""
        click.echo(expit.function(x))


class Utils(enum.Enum):

    utils = None

    @cached_property
    def data(self: Self) -> dict:
        text: str
        text = resources.read_text("preparse.tests", "expit.toml")
        return tomllib.loads(text)

    @staticmethod
    def istestable(x: Any) -> bool:
        if not isinstance(x, float):
            return True
        if not math.isnan(x):
            return True
        return False


class TestMainFunction(unittest.TestCase):

    def parse(
        self: Self,
        *,
        query: Any,
        exit_code: Any,
        output: Any,
        prog: Any,
        stdout: Any,
        stderr: Any,
    ) -> None:
        extra: dict
        result: Any
        runner: CliRunner
        runner = CliRunner()
        extra = dict()
        extra["cli"] = expit.main
        extra["args"] = query
        if Utils.istestable(prog):
            extra["prog_name"] = prog
        result = runner.invoke(**extra)
        if Utils.istestable(exit_code):
            self.assertEqual(exit_code, result.exit_code)
        if Utils.istestable(output):
            self.assertEqual(output, result.output)
        if Utils.istestable(stdout):
            self.assertEqual(stdout, result.stdout)
        if Utils.istestable(stderr):
            self.assertEqual(stderr, result.stderr)

    def test_0(self: Self) -> None:
        kwargs: dict
        name: str
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)


if __name__ == "__main__":
    unittest.main()

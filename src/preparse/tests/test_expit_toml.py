import enum
import math
import tomllib
import unittest
from functools import cached_property
from importlib import resources
from typing import Any, Self

from click.testing import CliRunner

from preparse._tests import expit

__all__ = ["TestMainFunction"]


class Utils(enum.Enum):
    utils = None

    @cached_property
    def data(self: Self) -> dict[str, Any]:
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
        extra: dict[Any, Any]
        result: Any
        runner: CliRunner
        runner = CliRunner()
        extra = dict()
        extra["cli"] = expit.main
        extra["args"] = query
        if Utils.utils.istestable(prog):
            extra["prog_name"] = prog
        result = runner.invoke(**extra)
        if Utils.utils.istestable(exit_code):
            self.assertEqual(exit_code, result.exit_code)
        if Utils.utils.istestable(output):
            self.assertEqual(output, result.output)
        if Utils.utils.istestable(stdout):
            self.assertEqual(stdout, result.stdout)
        if Utils.utils.istestable(stderr):
            self.assertEqual(stderr, result.stderr)

    def test_0(self: Self) -> None:
        kwargs: dict[Any, Any]
        name: str
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)


if __name__ == "__main__":
    unittest.main()

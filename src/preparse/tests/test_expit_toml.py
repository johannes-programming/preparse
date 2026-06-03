import enum
import math
import tomllib
import unittest
from importlib import resources
from typing import Any, Self

from click.testing import CliRunner

from preparse._tests import expit

__all__ = ["TestMainFunction"]


class Utils(enum.Enum):
    utils = None

    @staticmethod
    def get_data() -> dict[Any, Any]:
        data: dict[Any, Any]
        text: str
        text = resources.read_text("preparse.tests", "expit.toml")
        data = tomllib.loads(text)
        return data

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
        data: dict[Any, Any]
        kwargs: dict[Any, Any]
        name: str
        data = Utils.utils.get_data()
        for name, kwargs in data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)


if __name__ == "__main__":
    unittest.main()

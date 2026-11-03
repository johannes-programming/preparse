__all__: list[str] = ["TestDataToml"]

import enum
import functools
import io
import math
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

from preparse.core.PreParser import PreParser


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load and return the shared TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)

    @staticmethod
    def istestable(x: Any) -> bool:
        if not isinstance(x, float):
            return True
        if not math.isnan(x):
            return True
        return False


def getopt_settings(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Translate the unmodified legacy TOML options to getopt-style specs."""
    settings = dict(kwargs)
    allowslong = settings.pop("allowslong", True)
    allowsshort = settings.pop("allowsshort", True)
    optdict = settings.pop("optdict", {})
    shortsopts = "" if allowsshort else None
    longopts: list[str] | None = [] if allowslong else None
    for key, nargs in sorted(optdict.items()):
        # The old optdict treated 2 as an optional attached argument.
        short_suffix = ("", ":", "::")[nargs]
        long_suffix = ("", "=", "=?")[nargs]
        if key.startswith("--"):
            if longopts is not None:
                longopts.append(key[2:] + long_suffix)
            if shortsopts is not None and key == "--":
                shortsopts += "-" + short_suffix
        elif key.startswith("-"):
            if shortsopts is not None and len(key) == 2:
                shortsopts += key[1:] + short_suffix
            elif longopts is not None and shortsopts is None:
                # Single-dash long names are a legacy long-only extension.
                longopts.append(key + long_suffix)
    settings["shortsopts"] = shortsopts
    settings["longopts"] = None if longopts is None else tuple(longopts)
    return settings


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        kwargs: dict[str, Any]
        name: str
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**kwargs)

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        **kwargs: Any,
    ) -> None:
        answer: list[Any]
        capture: list[Any]
        data: dict[str, Any]
        erranswer: list[Any]
        msg: str
        parser: PreParser
        superanswer: list[Any]

        parser = PreParser(**getopt_settings(kwargs))
        data = dict(
            query=query,
            solution=solution,
            warnings=warnings,
            **kwargs,
        )
        answer, messages = parser.parse_args(query)
        erranswer = list(map(str, messages))
        superanswer = parser.parse_args(answer)[0]
        msg = "\n\ndata=%s,\nanswer=%s,\nsuperanswer=%s,\n\n" % (
            data,
            answer,
            superanswer,
        )
        self.assertEqual(answer, superanswer, msg=msg)
        msg = "\n\ndata=%s,\nanswer=%s,\nsolution=%s,\n\n" % (
            data,
            answer,
            solution,
        )
        self.assertEqual(answer, solution, msg=msg)
        if not Utils.utils.istestable(warnings):
            return
        msg = "\n\ndata=%s,\nerranswer=%s,\nwarnings=%s,\n\n" % (
            data,
            erranswer,
            warnings,
        )
        self.assertEqual(erranswer, warnings, msg=msg)


if __name__ == "__main__":
    unittest.main()

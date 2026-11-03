__all__: list[str] = ["TestDataToml"]

import enum
import functools
from collections.abc import Mapping
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


class TestDataToml(unittest.TestCase):

    def test_0(self: Self) -> None:
        kwargs: dict[str, Any]
        name: str
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                self.parse(**self.convert_specs(kwargs))

    @staticmethod
    def convert_specs(source: Mapping[str, Any]) -> dict[str, Any]:
        """Translate legacy TOML keys per table; never modify the TOML itself.

        A numeric value of 0 means a flag, 1 means required, and all
        other values mean optional, as in the preceding implementation.
        The optional mode uses the project's ``::``/``==`` extensions.
        """
        kwargs = dict(source)
        allowslong = bool(kwargs.pop("allowslong", True))
        allowsshort = bool(kwargs.pop("allowsshort", True))
        options = kwargs.pop("optdict", {})
        short_specs: list[str] = []
        long_specs: list[str] = []
        if isinstance(options, Mapping):
            entries = options.items()
        else:
            entries = options
        for key, mode in sorted(entries, key=lambda item: str(item[0])):
            key = str(key)
            mode = mode if isinstance(mode, int) and mode in (0, 1) else 2
            short_suffix = ("", ":", "::")[mode]
            long_suffix = ("", "=", "==")[mode]
            if allowsshort and key.startswith("-") and len(key) == 2:
                short_specs.append(key[1] + short_suffix)
            elif allowslong and key.startswith("--") and len(key) > 2:
                long_specs.append(key[2:] + long_suffix)
            elif allowslong and not allowsshort and key.startswith("-"):
                # Preserve old single-dash long-only configuration.
                long_specs.append(key + long_suffix)
        kwargs["shortsopts"] = "".join(short_specs) if allowsshort else None
        kwargs["longopts"] = tuple(long_specs) if allowslong else None
        return kwargs

    def test_legacy_table_conversion(self: Self) -> None:
        self.assertEqual(
            self.convert_specs({
                "query": [], "allowslong": True, "allowsshort": True,
                "optdict": {"-a": 0, "-b": 1, "-c": 2,
                            "--alpha": 0, "--beta": 1, "--gamma": 2},
            }),
            {"query": [], "shortsopts": "ab:c::",
             "longopts": ("alpha", "beta=", "gamma==")},
        )
        self.assertEqual(
            self.convert_specs({"allowslong": False, "allowsshort": False}),
            {"shortsopts": None, "longopts": None},
        )

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

        parser = PreParser(**kwargs)
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

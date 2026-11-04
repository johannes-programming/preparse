import enum
import functools
import io
import math
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

import tomli_w

from preparse.core.PreParser import PreParser
from preparse.enum.Depletion import Depletion


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load the converted TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent.parent / "tests" / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)

    @staticmethod
    def testvalue(x: Any) -> Any:
        if not isinstance(x, float):
            return x
        if not math.isnan(x):
            return x
        return None


def main() -> None:
    kwargs: dict[str, Any]
    name: str
    ans = dict()
    for name, kwargs in Utils.utils.data.items():
        ans[name] = parse(**kwargs)
    print(tomli_w.dumps(ans))


def parse(
    *,
    depletion: Any = "REINTERPRET",
    **kwargs: Any,
) -> dict[str, Any]:
    answer: list[Any]
    erranswer: list[Any]
    parser: PreParser

    if not isinstance(depletion, str):
        kwargs["depletion"] = depletion
        return kwargs
    kwargs_ = dict(kwargs)
    kwargs_.pop("query", None)
    kwargs_.pop("solution", None)
    kwargs_.pop("warnings", None)
    if isinstance(kwargs_["longopts"], float):
        kwargs_["longopts"] = None
    if isinstance(kwargs_["shortopts"], float):
        kwargs_["shortopts"] = None
    parser = PreParser(**kwargs_, depletion=Depletion.DROP)
    answer, messages = parser.parse_args(kwargs["query"])
    erranswer = list(map(str, messages))
    if answer != kwargs["solution"]:
        kwargs["depletion"] = depletion
        return kwargs
    if isinstance(kwargs["warnings"], float):
        kwargs["depletion"] = "DROP"
        return kwargs
    if erranswer != kwargs["warnings"]:
        kwargs["depletion"] = depletion
        return kwargs
    kwargs["depletion"] = "DROP"
    return kwargs


if __name__ == "__main__":
    main()

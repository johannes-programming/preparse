
import enum
import functools
import io
import math
import tomllib
import tomli_w
from pathlib import Path
from typing import Any, Self

from preparse.core.PreParser import PreParser
from preparse.enum.Depletion import Depletion


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load the converted TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent / "data.toml"
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
    data: dict[str, Any]
    data=dict()
    for name, kwargs in Utils.utils.data.items():
        data[name] = dict(kwargs)
        kwargs_ = dict()
        for x, y in kwargs.items():
            kwargs_[x] = Utils.testvalue(y)
        data[name]["depletion"]=parse(**kwargs_)
    print(tomli_w.dumps(data))


def parse(
    *,
    query: Any,
    solution: Any,
    warnings: Any,
    **kwargs: Any,
) -> str:
    answer: list[Any]
    erranswer: list[Any]
    parser: PreParser

    # TOML arrays become lists; TOML `false` stands for Python None,
    # which disables the corresponding option syntax in PreParser.
    parser = PreParser(**kwargs, depletion=Depletion.DROP)
    answer, messages = parser.parse_args(query)
    erranswer = list(map(str, messages))
    if answer != solution:
        return "REINTERPRET"
    if warnings is None:
        return "DROP"
    if erranswer != warnings:
        return "REINTERPRET"
    return "DROP"


if __name__ == "__main__":
    main()

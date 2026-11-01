import enum
import functools
import io
import math
import tomllib
from pathlib import Path
from typing import Any, Self

import tomli_w


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load and return the shared TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent.parent / "tests" / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)

    @staticmethod
    def istestable(x: Any) -> bool:
        if not isinstance(x, float):
            return True
        if not math.isnan(x):
            return True
        return False


def main() -> None:
    data: dict[str, Any]
    data = dict()
    for x, y in Utils.utils.data.items():
        data[x] = dict(y)
        data[x]["transformation"] = dict(data[x]["transformation"])
        data[x]["transformation"].setdefault("depletion", "DEFER")
    print(tomli_w.dumps(data))


main()

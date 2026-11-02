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

    @staticmethod
    def parser(
        *,
        allowslong: bool = True,
        allowsshort: bool = True,
        optdict: dict[str, int] = (),
        **kwargs: Any,
    ) -> dict[str, Any]:
        optdict = dict(optdict)
        if allowslong:
            kwargs["longopts"] = []
        else:
            kwargs["longopts"] = float("nan")
        if allowsshort:
            kwargs["shortopts"] = ""
        else:
            kwargs["shortopts"] = float("nan")
        if (allowslong, allowsshort) == (False, False):
            return kwargs
        for x, y in optdict.items():
            if not x.startswith("-"):
                continue
            if allowsshort:
                if len(x) == 2:
                    kwargs["shortopts"] += x[1]
                    kwargs["shortopts"] += ":" * y
                    continue
                if not x.startswith("--"):
                    continue
                z = x[2:]
            else:
                z = x[1:]
            if not allowslong:
                continue
            if y == 0:
                kwargs["longopts"].append(z)
            elif y == 1:
                kwargs["longopts"].append(z + "=")
            else:
                kwargs["longopts"].append(z + "=?")
        return kwargs


def main() -> None:
    data: dict[str, Any]
    data = dict()
    for x, y in Utils.utils.data.items():
        data[x] = Utils.parser(**y)
    print(tomli_w.dumps(data))


main()

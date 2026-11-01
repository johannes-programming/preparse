import enum
import functools
import io
import math
import sys
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
        z = dict(y)
        data[x] = dict()
        data[x]["legacy"] = dict()
        data[x]["testing"] = dict()
        data[x]["framework"] = dict()
        data[x]["transformation"] = dict()
        data[x]["optList"] = z.pop("optdict", {})
        data[x]["framework"]["allows_long"] = z.pop("allowslong", None)
        data[x]["framework"]["allows_short"] = z.pop("allowsshort", None)
        data[x]["framework"]["is_posix"] = z.pop("expectsposix", None)
        data[x]["transformation"]["bundling"] = z.pop("bundling", None)
        data[x]["transformation"]["special"] = z.pop("special", None)
        data[x]["transformation"]["abbr"] = {
            None: None,
            True: 0,
            False: 2,
        }[z.pop("expandsabbr", None)]
        data[x]["transformation"]["separate"] = z.pop("equal", None)
        data[x]["transformation"]["reconciles_orders"] = z.pop(
            "reconcilesorders", None
        )
        data[x]["legacy"]["prog"] = z.pop("prog", None)
        data[x]["legacy"]["expects_abbr"] = z.pop("expectsabbr", None)
        data[x]["testing"]["query"] = z.pop("query", None)
        data[x]["testing"]["solution"] = z.pop("solution", None)
        data[x]["testing"]["messages"] = list()
        warnings = z.pop("warnings", None)
        if Utils.istestable(warnings):
            data[x]["testing"]["messages"] = list()
            prefix = data[x]["legacy"]["prog"] + ": "
            for warning in warnings:
                if warning.startswith(prefix):
                    warning = warning[len(prefix) :]
                else:
                    raise ValueError(
                        f"Unexpected warning prefix in {x}: {warning}"
                    )
        else:
            data[x]["testing"]["messages"] = float("nan")
        if len(z):
            raise ValueError(f"Unexpected keys in {x}: {list(z.keys())}")
        for a, b in data[x].items():
            for c in list(b.keys()):
                if b[c] is None:
                    b.pop(c)
    print(tomli_w.dumps(data))


main()

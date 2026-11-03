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
    result = dict()
    for name, kwargs in Utils.utils.data.items():
        print(name, kwargs, file=sys.stderr)
        result[name] = parse(**kwargs)
    print(tomli_w.dumps(result))


def parse(
    *,
    query: Any,
    solution: Any,
    warnings: Any,
    allowslong: Any = True,
    allowsshort: Any = True,
    optdict: dict[str, int] | tuple[()] = (),
    expandsabbr: bool = True,
    expectsabbr: bool = True,
    expectsposix: bool = False,
    bundling: int = 2,
    special: int = 2,
    prog: str | None = None,
    reconcilesorders: bool = True,
) -> dict[str, Any]:
    ans = dict()
    ans["query"] = query
    ans["solution"] = solution
    if isinstance(warnings, list):
        ans["warnings"] = list()
        for x in warnings:
            z = prog + ": "
            if not x.startswith(z):
                raise ValueError
            ans["warnings"].append(x[len(z) :])
    else:
        ans["warnings"] = warnings
    ans["shortopts"] = "" if allowsshort else float("nan")
    ans["longopts"] = [] if allowslong else float("nan")
    optdict = dict(optdict)
    if not (allowslong or allowsshort):
        optdict.clear()
    for x, y in dict(optdict).items():
        if not x.startswith("-"):
            continue
        if allowsshort:
            if len(x) == 2:
                ans["shortopts"] += x[1]
                ans["shortopts"] += ":" * min(y, 2)
                continue
        if not allowslong:
            continue
        if allowsshort:
            if not x.startswith("--"):
                continue
            z = x[2:]
        else:
            z = x[1:]
        if y == 0:
            ans["longopts"].append(z)
        elif y == 1:
            ans["longopts"].append(z + "=")
        else:
            ans["longopts"].append(z + "=?")
    ans["expandsabbr"] = expandsabbr
    ans["is_posix"] = expectsposix
    ans["bundling"] = bundling
    ans["special"] = special
    ans["reconcilesorders"] = reconcilesorders

    return ans


if __name__ == "__main__":
    main()

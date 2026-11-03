"""Convert tests/data.toml to the getopt-style PreParser configuration.

Requires Python 3.11+ and ``tomli-w`` (``python -m pip install tomli-w``).

Place this file in the project's ``tests`` directory and run::

    python tests/convert_data_toml.py

By default, this converts ``tests/data.toml`` in place. To keep the original,
pass ``--output tests/data.converted.toml`` instead. The conversion is
idempotent: running it again does not re-interpret converted test cases.

TOML has no null value, so ``false`` represents ``None`` (disabled parsing)
for ``shortsopts`` and ``longopts``. Other values use the PreParser format:
a getopt-style string for short options and an array for long options.
"""

from __future__ import annotations

import enum
import functools
import io
import tomllib
from pathlib import Path
from typing import Any, Self

import tomli_w


def convert_case(*, prog: Any = None, **case: Any) -> dict[str, Any]:
    if prog is None:
        if isinstance(case["warnings"], list):
            raise ValueError
        else:
            return case
    if not isinstance(case["warnings"], list):
        return case
    warnings = list(case["warnings"])
    case["warnings"] = []
    prefix = prog + ": "
    for w in warnings:
        if not w.startswith(prefix):
            raise ValueError
        case["warnings"].append(w[len(prefix) :])
    return case


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


def main() -> None:

    converted = {
        name: convert_case(**case) for name, case in Utils.utils.data.items()
    }
    result = tomli_w.dumps(converted)
    # Reject malformed output before changing the source file.
    print(result)


if __name__ == "__main__":
    main()

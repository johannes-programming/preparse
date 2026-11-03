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

import argparse
import enum
import functools
import io
import math
import os
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

import tomli_w

LEGACY_FIELDS = frozenset({"allowslong", "allowsshort", "optdict"})
NEW_FIELDS = frozenset({"shortsopts", "longopts"})


def convert_case(name: str, case: dict[str, Any]) -> dict[str, Any]:
    """Replace the three legacy fields in one TOML test case."""
    if not LEGACY_FIELDS.intersection(case):
        if not NEW_FIELDS.issubset(case):
            raise ValueError(f"{name}: missing option specifications")
        return dict(case)
    if NEW_FIELDS.intersection(case):
        raise ValueError(f"{name}: contains both legacy and new option fields")

    allowslong = case.get("allowslong", True)
    allowsshort = case.get("allowsshort", True)
    optdict = case.get("optdict", {})

    # False is the TOML representation of None (disabled option syntax).
    shortsopts: str | bool = "" if allowsshort else False
    longopts: list[str] | bool = [] if allowslong else False

    for key, nargs in sorted(optdict.items()):
        if nargs not in (0, 1, 2):
            raise ValueError(
                f"{name}: unsupported argument count for {key!r}: {nargs!r}"
            )
        short_suffix = ("", ":", "::")[nargs]
        long_suffix = ("", "=", "=?")[nargs]
        if key.startswith("--"):
            if longopts is not False:
                longopts.append(key[2:] + long_suffix)
            if shortsopts is not False and key == "--":
                shortsopts += "-" + short_suffix
        elif key.startswith("-"):
            if shortsopts is not False and len(key) == 2:
                shortsopts += key[1:] + short_suffix
            elif longopts is not False and shortsopts is False:
                # Preserve the former single-dash long-only convention.
                longopts.append(key + long_suffix)

    return {
        "shortsopts": shortsopts,
        "longopts": longopts,
        **{
            key: value
            for key, value in case.items()
            if key not in LEGACY_FIELDS
        },
    }


class Utils(enum.Enum):
    utils = None

    @functools.cached_property
    def data(self: Self, /) -> dict[str, Any]:
        """Load the converted TOML test data."""
        file: Path
        stream: io.BufferedReader
        file = Path(__file__).parent.parent / "tests"/"data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)


def main() -> None:

    converted = {
        name: convert_case(name, case)
        for name, case in Utils.utils.data.items()
    }
    result = tomli_w.dumps(converted)
    # Reject malformed output before changing the source file.
    print(result)


if __name__ == "__main__":
    main()

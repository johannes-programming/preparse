

import enum
import math
import tomllib
import unittest
import functools
import io
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


class Main(unittest.TestCase):

    def main(self: Self) -> None:
        kwargs: dict[str, Any]
        name: str
        ans=dict()
        for name, kwargs in Utils.utils.data.items():
            with self.subTest(msg=name, **kwargs):
                ans[name]=self.parse(**kwargs)
        text = tomli_w.dumps(ans)
        print(text)

    def parse(
        self: Self,
        *,
        query: Any,
        solution: Any,
        warnings: Any,
        optdict: Any,
        allowslong:Any,
        allowsshort:Any,
        bundling:Any,
        expandsabbr:Any,
        expectsabbr:Any,
        expectsposix:Any,
        prog:Any,
        reconcilesorders:Any,
        special:Any,
    ):
        legacy=dict(special=special, prog=prog, expectsabbr=expectsabbr)
        framework=dict(
            allows_long=allowslong,
            allows_short=allowsshort,
            is_posix=expectsposix,
        )
        transformation=dict(
            bundling=bundling,
            order_compatibility=1 if reconcilesorders else 2,
            abbr=0 if expandsabbr else 2,
        )
        testing=dict(query=query, solution=solution, warnings=warnings)
        return dict(
            legacy=legacy,
            optDict=optdict,
            framework=framework,
            transformation=transformation,
            testing=testing,
        )

Main().main()
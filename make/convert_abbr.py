import enum
import functools
import io
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
        file = Path(__file__).parent.parent / "tests" / "data.toml"
        with file.open("rb") as stream:
            return tomllib.load(stream)


def main() -> None:
    kwargs: dict[str, Any]
    name: str
    ans = dict()
    for name, kwargs in Utils.utils.data.items():
        ans[name] = parse(**kwargs)
    print(tomli_w.dumps(ans))


def parse(
    *,
    expandsabbr: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    if expandsabbr:
        kwargs["abbr"] = 0
    else:
        kwargs["abbr"] = 2
    return kwargs


if __name__ == "__main__":
    main()

"""Translate getopt-style option specifications into internal argument modes.

The standard Python getopt formats are supported: ``a:`` for a short
option requiring a value and ``long=`` for a long option requiring a value.
For compatibility with the old parser's optional-argument mode, ``a::``
and ``long==`` additionally indicate an *optional attached* argument.
An optional argument never consumes the following argv element.
"""

__all__: list[str] = ["option_modes"]

NO_ARGUMENT = 0
REQUIRED_ARGUMENT = 1
OPTIONAL_ARGUMENT = 2


def option_modes(
    shortsopts: str | None, longopts: tuple[str, ...] | None
) -> dict[str, int]:
    """Build an internal lookup table without exposing an option dictionary API."""
    modes: dict[str, int] = {}
    if shortsopts is not None:
        position = 0
        while position < len(shortsopts):
            char = shortsopts[position]
            position += 1
            if char == ":":
                continue
            trailing = 0
            while position < len(shortsopts) and shortsopts[position] == ":":
                trailing += 1
                position += 1
            modes.setdefault(
                "-" + char,
                (OPTIONAL_ARGUMENT if trailing >= 2 else REQUIRED_ARGUMENT)
                if trailing else NO_ARGUMENT,
            )
    if longopts is not None:
        for item in longopts:
            if item.endswith("=="):
                name, mode = item[:-2], OPTIONAL_ARGUMENT
            elif item.endswith("="):
                name, mode = item[:-1], REQUIRED_ARGUMENT
            else:
                name, mode = item, NO_ARGUMENT
            # Python getopt accepts bare long names, not leading '--'.
            # With short parsing disabled, an explicit '-name' is useful for
            # legacy single-dash long-only mode.
            key = name if name.startswith("-") else "--" + name
            modes.setdefault(key, mode)
    return modes

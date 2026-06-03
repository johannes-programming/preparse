from typing import Any, Callable, Protocol


class Parser(Protocol):
    parse_args: Callable[..., Any]

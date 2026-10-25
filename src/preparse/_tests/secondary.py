from typing import Any

import click

__all__ = ["secondary"]


@click.command()
@click.option("-v", "--verbose", is_flag=True)
@click.option("--name", required=True)
@click.option("--color/--no-color", default=True)
@click.option("--mode", is_flag=False, flag_value="auto", default=None)
def secondary(**kwargs: Any) -> None:
    i: tuple[str, Any]
    for i in sorted(kwargs.items()):
        print("%s = %r" % i)

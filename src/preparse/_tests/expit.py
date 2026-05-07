import math
from typing import *

import click

from preparse.core import *

__all__ = ["function", "main"]


def function(x: float) -> float:
    p: float
    try:
        p = math.exp(-x)
    except OverflowError:
        p = float("+inf")
    return 1 / (1 + p)


@PreParser(reconcilesorders=True, expectsposix=False).click()
@click.command(add_help_option=False)
@click.help_option("-h", "--help")
@click.version_option("1.2.3", "-V", "--version")
@click.argument("x", type=float)
def main(x: float) -> None:
    """applies the expit function to x"""
    click.echo(function(x))

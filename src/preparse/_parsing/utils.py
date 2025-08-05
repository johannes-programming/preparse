from typing import *

__all__ = [
    "might_be_an_option",
]

def might_be_an_option(arg:str)->bool:
    return arg != "-" and arg.startswith("-")
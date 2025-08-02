import dataclasses
import functools
from typing import *

from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["Item"]

@dataclasses.dataclass
class Item:
    key:Optional[str]=None
    equal:bool=False
    value:Optional[str]=None
    comment:Any=None
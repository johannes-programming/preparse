from preparse._parsing.Item import *
from typing import *
if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser
__all__ = ["digest"]

def digest(*, items:list[Item], parser:"PreParser")->list[Item]:
    ...
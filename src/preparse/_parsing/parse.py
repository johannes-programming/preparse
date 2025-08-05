from preparse._parsing.Item import *
from typing import *
if TYPE_CHECKING:
    from preparse.core.PreParser import PreParser
__all__ = ["parse"]

def parse(*, args:list[str], parser:"PreParser")->list[Item]:
    ...
from preparse._processing.deparsing import *
from preparse._processing.digesting import *
from preparse._processing.parsing import *
from preparse._processing.pulling import *
from preparse.core.enums import *
from types import FunctionType

__all__ = ["process"]


def process(
    # pull
    args: Optional[Iterable] = None, *, 

    # options
    allowslong:bool,
    allowsshort:bool,
    optdict:dict,

    # warnings
    prog:str,
    warn:FunctionType,

    # orders
    expectsposix:bool,
    reconcileorders:bool,

    # abbr
    expectsabbr:bool,
    expandsabbr:bool,

    # tuning
    bundling:Tuning,
    special:Tuning,
    
) -> list[str]:
    "This method parses args."
    items: list[Item] = pull(args)
    items = parse(
        items, 
        allowslong=allowslong,
        allowsshort=allowsshort,
        expectsabbr=expectsabbr,
        expectsposix=expectsposix,
        optdict=optdict,
        prog=prog,
        warn=warn,
    )
    items = digest(
        items, 
        allowslong=allowslong, 
        bundling=bundling,
        expandsabbr=expandsabbr,
        expectsposix=expectsposix,
        reconcileorders=reconcileorders,
        special=special,
    )
    ans:list[str] = deparse(items)
    return ans

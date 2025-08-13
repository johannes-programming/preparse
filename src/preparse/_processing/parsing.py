from types import FunctionType
from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["parse"]

PUOW = PreparseUnrecognizedOptionWarning
PAOW = PreparseAmbiguousOptionWarning
PUAW = PreparseUnallowedArgumentWarning
PIOW = PreparseInvalidOptionWarning
PLORAW = PreparseLongOptionRequiresArgumentWarning
PSORAW = PreparseShortOptionRequiresArgumentWarning


def parse(
    items: list[Positional],
    *,
    allowslong: bool,
    allowsshort: bool,
    expectsabbr: bool,
    expectsposix: bool,
    prog: str,
    warn: FunctionType,
    **kwargs: Any,
) -> list[Item]:
    if not (allowslong and allowsshort):
        return list(items)
    ans: list[Item] = list()
    broken: bool = False
    cause_warning: FunctionType = parse_cause(prog=prog, warn=warn)
    hungry: bool = False
    item: Positional
    opt: Optional[Option] = None
    for item in items:
        if broken:
            ans.append(item)
            continue
        if hungry:
            ans[-1].right = item.value
            hungry = False
            continue
        if item.iscomp():
            ans.append(item)
            broken = expectsposix
            continue
        if item.value == "--":
            ans.append(Special())
            broken = True
            continue
        if item.value.startswith("--") and allowslong:
            opt = parse_long(
                item.value,
                cause_warning=cause_warning,
                expectsabbr=expectsabbr,
                **kwargs,
            )
        else:
            opt = parse_bundle(
                item.value,
                cause_warning=cause_warning,
                **kwargs,
            )
        hungry = opt.nargs == Nargs.REQUIRED_ARGUMENT and opt.right is None
        ans.append(opt)
    if not hungry:
        pass
    elif isinstance(ans[-1], Long):
        cause_warning(PLORAW, option=ans[-1].left)
    else:
        cause_warning(PSORAW, option="-" + ans[-1].left[-1])
    return ans


def parse_bundle(
    arg: str,
    *,
    optdict: dict,
    cause_warning: FunctionType,
) -> Bundle:
    ans: Bundle = Bundle(left="")
    i: int
    a: str
    opt: str
    for i, a in enumerate(arg):
        ans.left += a
        if i == 0:
            continue
        opt = "-" + a
        if opt not in optdict.keys():
            cause_warning(PIOW, option=opt)
            continue
        ans.nargs = optdict[opt]
        if ans.nargs == Nargs.NO_ARGUMENT:
            continue
        if i + 1 < len(arg):
            ans.right = arg[i + 1 :]
            ans.joined = True
        break
    return ans


def parse_cause(*, prog: str, warn: FunctionType) -> FunctionType:
    def ans(cls: type, **kwargs: Any) -> None:
        warn(cls(prog=prog, **kwargs))

    return ans


def parse_long(
    arg: str,
    *,
    expectsabbr: bool,
    optdict: dict,
    cause_warning: FunctionType,
) -> Long:
    ans: Item = Long(left=arg)
    if "=" in arg:
        ans.left, ans.right = arg.split("=", 1)
        ans.joined = True
    if ans.left in optdict.keys():
        ans.nargs = optdict[ans.left]
        return ans
    if not expectsabbr:
        cause_warning(PUOW, option=arg)
        return ans
    matches = list()
    k: str
    for k in optdict.keys():
        if k.startswith(arg):
            matches.append(k)
    if len(matches) == 0:
        cause_warning(PUOW, option=arg)
        return ans
    if len(matches) > 1:
        cause_warning(PAOW, option=arg, possibilities=matches)
        return ans
    ans.abbrlen = len(ans.left)
    (ans.left,) = matches
    ans.nargs = optdict[ans.left]
    return ans

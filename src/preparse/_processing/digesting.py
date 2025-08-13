from typing import *

from preparse._processing.items import *
from preparse.core.enums import *

__all__ = ["digest"]


def digest(
    items: list[Item],
    *,
    allowslong: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsposix: bool,
    reconcilesorders: bool,
    special: Special,
) -> list[Item]:
    ans: list[Item] = list(items)
    ans = digest_order(
        items,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
    )
    ans = digest_abbr(ans, expandsabbr=expandsabbr)
    ans = digest_bundling(ans, bundling=bundling, allowslong=allowslong)
    ans = digest_special(ans, special=special)
    return ans


def digest_abbr(items: list[Item], *, expandsabbr: bool) -> list[Item]:
    ans: list[Item] = list(items)
    if not expandsabbr:
        return ans
    for x in ans:
        if isinstance(x, Long):
            x.abbrlen = None
    return ans


def digest_bundling(
    items: list[Item], *, bundling: Tuning, allowslong: bool
) -> list[Item]:
    if bundling == Tuning.MINIMIZE:
        return digest_bundling_min(items, allowslong=allowslong)
    if bundling == Tuning.MAXIMIZE:
        return digest_bundling_max(items)
    return list(items)


def digest_bundling_max(items: list[Item]) -> list[Item]:
    ans: list[Item] = [Special()]
    item: Item
    for item in items:
        if not isinstance(ans[-1], Bundle):
            ans.append(item)
            continue
        if not isinstance(item, Bundle):
            ans.append(item)
            continue
        if ans[-1].nargs != Nargs.NO_ARGUMENT:
            ans.append(item)
            continue
        item.left = ans[-1].left + item.left[1:]
        ans[-1] = item
    ans.pop(0)
    return ans


def digest_bundling_min(items: list[Item], allowslong: bool) -> list[Item]:
    ans: list[Item] = list()
    item: Item
    parts: list[str]
    x: str
    for item in items:
        if not isinstance(item, Bundle):
            ans.append(item)
            continue
        x = item.left[1:]
        if allowslong:
            parts = digest_bundling_min_split_str_allowslong(x)
        else:
            parts = digest_bundling_min_split_str_allowslong(x)
        for x in parts:
            ans.append(Bundle(left="-" + x))
    return ans


def digest_bundling_min_split_str_allowslong(whole: str) -> list[str]:
    ans: list[str] = list()
    x: str
    for x in whole:
        if x == "-":
            ans[-1] += "-"
        else:
            ans.append(x)
    return x


def digest_bundling_min_split_str_shortonly(whole: str) -> list[str]:
    ans: list[str] = list()
    x: str = whole
    while x:
        if x == "-":
            ans[0] = "-" + ans[0]
            x = ""
        elif x.endswith("-"):
            ans.insert(0, x[-2:])
            x = x[:-2]
        else:
            ans.insert(0, x[-1])
            x = x[:-1]
    return ans


def digest_order(
    items: list[Item],
    *,
    expectsposix: bool,
    reconcilesorders: bool,
) -> list[Item]:
    ans: list[Item] = list(items)
    if not reconcilesorders:
        return ans
    if not expectsposix:
        ans.sort(key=digest_order_sortkey)
        return ans
    comp: bool = True
    i: int = len(ans)
    while True:
        i -= 1
        if i == -1:
            break
        if isinstance(ans[i], Special):
            return ans
        if isinstance(ans[i], Option):
            break
        if ans[i].value.startswith("-") and ans[i].value != "-":
            comp = False
    if not comp:
        ans.insert(i + 1, Special())
    return ans


def digest_order_sortkey(item: Item) -> int:
    return item.sortkey()


def digest_special(items: list[Item], *, special: Tuning) -> list[Item]:
    if special == Tuning.MINIMIZE:
        return digest_special_min(items)
    if special == Tuning.MAXIMIZE:
        return digest_special_max(items)
    return list(items)


def digest_special_max(items: list[Item]) -> list[Item]:
    ans: list[Item] = list(items)
    i: int = len(ans)
    while True:
        i -= 1
        if i == -1:
            break
        if isinstance(ans[i], Option):
            break
        if isinstance(ans[i], Special):
            return ans
    ans.insert(i + 1, Special())
    return ans


def digest_special_min(items: list[Item]) -> list[Item]:
    ans: list[Item] = list(items)
    comp: bool = True
    while True:
        i -= 1
        if i == -1:
            return ans
        if isinstance(ans[i], Option):
            return ans
        if isinstance(ans[i], Positional):
            comp &= ans[i].iscomp()
            continue
        if comp:
            ans.pop(i)
        return ans

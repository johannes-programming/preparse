from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["digest"]


def digest(
    items: list[Item],
    *,
    allowslong: bool,
    bundling: Tuning,
    expandsabbr: bool,
    expectsposix: bool,
    reconcilesorders: bool,
    special: Tuning,
) -> list[Item]:
    ans: list[Item] = list(items)
    ans = digest_abbr(ans, expandsabbr=expandsabbr)
    ans = digest_special(
        ans,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    ans = digest_order(
        items,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
    )
    ans = digest_bundling(ans, bundling=bundling, allowslong=allowslong)
    return ans


def digest_abbr(
    items: list[Item],
    *,
    expandsabbr: bool,
) -> list[Item]:
    ans: list[Item] = list(items)
    if not expandsabbr:
        return ans
    item: Item
    for item in ans:
        if isinstance(item, Long):
            item.abbrlen = None
    return ans


def digest_bundling(
    items: list[Item],
    *,
    allowslong: bool,
    bundling: Tuning,
) -> list[Item]:
    if bundling == Tuning.MINIMIZE:
        return digest_bundling_min(items, allowslong=allowslong)
    if bundling == Tuning.MAXIMIZE:
        return digest_bundling_max(items)
    return items


def digest_bundling_min(items: list[Item], *, allowslong: bool) -> list[Item]:
    ans: list[Item] = list()
    item: Item
    for item in items:
        if isinstance(item, Bundle):
            ans += item.split(allowslong=allowslong)
        else:
            ans.append(item)
    return ans


def digest_bundling_max(items: list[Item]) -> list[Item]:
    ans: list[Item] = list()
    item: Item
    for item in items:
        if not isinstance(item, Bundle):
            ans.append(item)
            continue
        if len(ans) == 0:
            ans.append(item)
            continue
        if not isinstance(ans[-1], Bundle):
            ans.append(item)
            continue
        if ans[-1].right is not None:
            ans.append(item)
            continue
        item.chars = ans[-1].chars + item.chars
        ans[-1] = item
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
        ans.sort(key=digest_order_key)
        return ans
    i: int = len(ans)
    comp: bool = True
    while True:
        i -= 1
        if i == -1:
            break
        if isinstance(ans[i], Option):
            break
        if isinstance(ans[i], Special):
            comp = True
            break
        if not ans[i].isobvious():
            comp = False
    if not comp:
        ans.insert(i + 1, Special())
    return ans


def digest_order_key(item: Item) -> int:
    return item.sortkey()


def digest_special(items: list[Item], *, special: Tuning, **kwargs: Any) -> list[Item]:
    if special == Tuning.MINIMIZE:
        return digest_special_min(items, **kwargs)
    if special == Tuning.MAXIMIZE:
        return digest_special_max(items)
    return list(items)


def digest_special_min(
    items: list[Item],
    expectsposix: bool,
    reconcilesorders: bool,
) -> list[Item]:
    if expectsposix and not reconcilesorders:
        return digest_special_min_posix(items)
    else:
        return digest_special_min_nonposix(items)


def digest_special_min_nonposix(
    items: list[Item],
) -> list[Item]:
    raise NotImplementedError


def digest_special_min_posix(
    items: list[Item],
) -> list[Item]:
    ans: list[Item] = list(items)
    deletable: bool = True
    i: int = len(items)
    while True:
        i -= 1
        if i == -1:
            deletable = False
            break
        if isinstance(ans[i], Option):
            deletable = False
            break
        if isinstance(ans[i], Special):
            break
        deletable = ans[i].isobvious()
    if deletable:
        ans.pop(i)
    return ans


def digest_special_max(items: list[Item]) -> list[Item]:
    raise NotImplementedError  # remember hungry option

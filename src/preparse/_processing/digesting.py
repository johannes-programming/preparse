from typing import *

from preparse._processing.items.Bundle import Bundle
from preparse._processing.items.Item import Item
from preparse._processing.items.Long import Long
from preparse._processing.items.Option import Option
from preparse._processing.items.Positional import Positional
from preparse._processing.items.Special import Special
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
    ans: list[Item]
    ans = list(items)
    ans = digest_abbr(
        ans,
        expandsabbr=expandsabbr,
    )
    ans = digest_special(
        ans,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    ans = digest_order(
        ans,
        expectsposix=expectsposix,
        reconcilesorders=reconcilesorders,
    )
    ans = digest_bundling(
        ans,
        bundling=bundling,
        allowslong=allowslong,
    )
    return ans


def digest_abbr(
    items: list[Item],
    *,
    expandsabbr: bool,
) -> list[Item]:
    ans: list[Item]
    item: Item
    ans = list(items)
    if not expandsabbr:
        return ans
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


def digest_bundling_min(
    items: list[Item],
    *,
    allowslong: bool,
) -> list[Item]:
    ans: list[Item]
    item: Item
    ans = list()
    for item in items:
        if isinstance(item, Bundle):
            ans += item.split(allowslong=allowslong)
        else:
            ans.append(item)
    return ans


def digest_bundling_max(items: list[Item]) -> list[Item]:
    ans: list[Item]
    item: Item
    ans = list()
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
    ans: list[Item]
    comp: bool
    index: int
    ans = list(items)
    if not reconcilesorders:
        return ans
    if not expectsposix:
        ans.sort(key=digest_order_key)
        return ans
    index = len(ans)
    comp = True
    while True:
        index -= 1
        if index == -1:
            break
        if isinstance(ans[index], Option):
            break
        if isinstance(ans[index], Special):
            comp = True
            break
        if not ans[index].isobvious():
            comp = False
    if not comp:
        ans.insert(index + 1, Special())
    return ans


def digest_order_key(item: Item) -> int:
    return item.sortkey()


def digest_special(
    items: list[Item],
    *,
    special: Tuning,
    **kwargs: Any,
) -> list[Item]:
    if special == Tuning.MINIMIZE:
        return digest_special_min(items, **kwargs)
    if special == Tuning.MAXIMIZE:
        return digest_special_max(items)
    return list(items)


def digest_special_max(items: list[Item]) -> list[Item]:
    ans: list[Item]
    index: int
    ans = list(items)
    index = len(items)
    while True:
        index -= 1
        if index == -1:
            break
        if isinstance(ans[index], Special):
            break
        if isinstance(ans[index], Positional):
            continue
        if ans[index].ishungry():
            ans[index].joined = False
            ans[index].right = "--"
        ans.insert(index + 1, Special())
        break
    return ans


def digest_special_min(
    items: list[Item],
    *,
    expectsposix: bool,
    reconcilesorders: bool,
) -> list[Item]:
    ans: list[Item]
    index: int
    isdel: bool
    isposix: bool
    ans = list(items)
    isdel = True
    isposix = expectsposix and not reconcilesorders
    index = len(items)
    while True:
        index -= 1
        if index == -1:
            isdel = False
            break
        if isinstance(ans[index], Option):
            isdel = False
            break
        if isinstance(ans[index], Special):
            break
        isdel = ans[index].isobvious()
        if not (isdel or isposix):
            break
    if isdel:
        ans.pop(index)
    return ans

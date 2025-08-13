from typing import *

from preparse._processing.items import *
from preparse.core.enums import *
from preparse.core.warnings import *

__all__ = ["digest"]


def digest(
    items: list[Item],
    *,
    special: Tuning,
    reconcilesorders: bool,
    expectsposix: bool,
    bundling: Tuning,
) -> list[Item]:
    if special != Tuning.MAINTAIN:
        raise NotImplementedError
    items = list(
        digest_order(
            items,
            expectsposix=expectsposix,
            reconcilesorders=reconcilesorders,
        )
    )
    items = list(digest_bundling(items=items, bundling=bundling))
    return items


def digest_bundling(*, items: list[Item], bundling: Tuning) -> list[Item]:
    if bundling == Tuning.MINIMIZE:
        return digest_bundling_minimize(items)
    if bundling == Tuning.MAXIMIZE:
        return digest_bundling_maximize(items)
    return items


def digest_bundling_minimize(items: list[Item]) -> list[Item]:
    ans: list[Item] = list()
    item: Item
    for item in items:
        ans += digest_bundling_minimize_split(item)
    return ans


def digest_bundling_minimize_split(item: Item) -> list[Item]:
    if not isinstance(item, Option):
        return [item]
    if not item.isbundle():
        return [item]
    ans: list[Item] = list()
    x: str
    for x in item.left:
        if x == "-":
            ans[-1].left += "-"
        else:
            ans.append(Option(left=x))
    item.left = ans[-1].left
    ans[-1] = item
    return ans


def digest_bundling_maximize(items: list[Item]) -> list[Item]:
    ans: list[Item] = list()
    item: Item
    for item in items:
        if not isinstance(item, Option):
            ans.append(item)
            continue
        if not item.isbundle():
            ans.append(item)
            continue
        if len(ans) == 0:
            ans.append(item)
            continue
        if not isinstance(ans[-1], Option):
            ans.append(item)
            continue
        if not ans[-1].isbundle():
            ans.append(item)
            continue
        if ans[-1].value is not None:
            ans.append(item)
            continue
        item.left = ans[-1].left + item.left
        ans[-1] = item
    return ans


def digest_order(
    items: list[Item], *, expectsposix: bool, reconcilesorders: bool
) -> list[Item]:
    ans: list[Item] = list(items)
    if not reconcilesorders:
        return ans
    if not expectsposix:
        ans.sort(key=digest_order_key)
        return ans
    raise NotImplementedError


def digest_order_key(item: Item) -> int:
    return item.sortkey()

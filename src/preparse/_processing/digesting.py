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
    if not item.isbundle():
        return [item]
    ans: list[Item] = list()
    x: str
    for x in item.key:
        if x == "-":
            ans[-1].key += "-"
        else:
            ans.append(Item(key=x))
    item.key = ans[-1].key
    ans[-1] = item
    return ans


def digest_bundling_maximize(items: list[Item]) -> list[Item]:
    ans: list[Item] = [items.pop(0)]
    item: Item
    for item in items:
        if item.isbundle() and ans[-1].isbundle() and ans[-1].value is None:
            item.key = ans[-1].key + item.key
            ans[-1] = item
        else:
            ans.append(item)
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


def digest_order_key(item: Item):
    if item.isoption():
        return 0
    if item.isspecial():
        return 1
    return 2

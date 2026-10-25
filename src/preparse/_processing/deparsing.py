__all__: list[str] = ["deparse"]

from typing import *

from preparse._items.Item import Item


def deparse(items: list[Item]) -> list[str]:
    ans: list[str]
    item: Item
    ans = list()
    for item in items:
        ans += item.deparse()
    return ans

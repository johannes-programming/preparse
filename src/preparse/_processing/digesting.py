__all__: list[str] = ["digest"]

from typing import Any

from preparse._items.Bundle import Bundle
from preparse._items.Item import Item
from preparse._items.Long import Long
from preparse._items.Option import Option
from preparse._items.Positional import Positional
from preparse._items.Special import Special
from preparse.enum.Tuning import Tuning


def digest(
    items: list[Item],
    *,
    long_enabled: bool,
    short_enabled: bool,
    bundling: Tuning,
    abbr: Tuning,
    longopts: tuple[str, ...] | None,
    is_posix: bool,
    reconcilesorders: bool,
    special: Tuning,
) -> list[Item]:
    ans: list[Item]
    ans = list(items)
    ans = digest_abbr(
        ans,
        abbr=abbr,
        longopts=longopts,
        short_enabled=short_enabled,
    )
    ans = digest_special(
        ans,
        long_enabled=long_enabled,
        short_enabled=short_enabled,
        is_posix=is_posix,
        reconcilesorders=reconcilesorders,
        special=special,
    )
    ans = digest_order(
        ans,
        long_enabled=long_enabled,
        short_enabled=short_enabled,
        is_posix=is_posix,
        reconcilesorders=reconcilesorders,
    )
    ans = digest_bundling(
        ans,
        bundling=bundling,
        long_enabled=long_enabled,
    )
    return ans


def digest_abbr(
    items: list[Item],
    *,
    abbr: Tuning,
    longopts: tuple[str, ...] | None,
    short_enabled: bool,
) -> list[Item]:
    ans: list[Item]
    item: Item
    option: str
    options: list[str]
    ans = list(items)
    if abbr == Tuning.MAINTAIN:
        return ans
    options = list()
    for spec in longopts or ():
        option = digest_long_fullkey(spec, short_enabled=short_enabled)
        options.append(option)
    for item in ans:
        if not isinstance(item, Long):
            continue
        if abbr == Tuning.MINIMIZE:
            item.abbrlen = None
            continue
        if item.fullkey not in options:
            continue
        for length in range(2, len(item.fullkey) + 1):
            candidate = item.fullkey[:length]
            if candidate == "--":
                continue
            if candidate == item.fullkey:
                item.abbrlen = length
                break
            if [item.fullkey] == [
                key for key in options if key.startswith(candidate)
            ]:
                item.abbrlen = length
                break
    return ans


def digest_bundling(
    items: list[Item],
    *,
    long_enabled: bool,
    bundling: Tuning,
) -> list[Item]:
    if bundling == Tuning.MINIMIZE:
        return digest_bundling_min(items, long_enabled=long_enabled)
    if bundling == Tuning.MAXIMIZE:
        return digest_bundling_max(items)
    return items


def digest_bundling_min(
    items: list[Item],
    *,
    long_enabled: bool,
) -> list[Item]:
    ans: list[Item]
    item: Item
    ans = list()
    for item in items:
        if isinstance(item, Bundle):
            ans += item.split(long_enabled=long_enabled)
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
    long_enabled: bool,
    short_enabled: bool,
    is_posix: bool,
    reconcilesorders: bool,
) -> list[Item]:
    ans: list[Any]
    comp: bool
    index: int
    ans = list(items)
    if not (long_enabled or short_enabled):
        return ans
    if not reconcilesorders:
        return ans
    if not is_posix:
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
    **kwargs: bool,
) -> list[Item]:
    if special == Tuning.MINIMIZE:
        return digest_special_min(items, **kwargs)
    if special == Tuning.MAXIMIZE:
        return digest_special_max(items)
    return list(items)


def digest_special_max(items: list[Item]) -> list[Item]:
    ans: list[Any]
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
    long_enabled: bool,
    short_enabled: bool,
    is_posix: bool,
    reconcilesorders: bool,
) -> list[Item]:
    ans: list[Any]
    index: int
    isdel: bool
    isposix: bool
    ans = list(items)
    isdel = True
    isposix = is_posix and not (
        reconcilesorders and (long_enabled or short_enabled)
    )
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


def digest_long_fullkey(spec: str, *, short_enabled: bool) -> str:
    if short_enabled:
        ans = "--" + spec
    else:
        ans = "-" + spec
    if ans.endswith("=?"):
        return ans[:-2]
    if ans.endswith("="):
        return ans[:-1]
    return ans

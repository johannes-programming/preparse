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
    abbr: Tuning,
    bundling: Tuning,
    is_posix: bool,
    joined: Tuning,
    long_enabled: bool,
    longopts: tuple[str, ...] | None,
    reconciles_orders: bool,
    short_enabled: bool,
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
    ans = digest_joined(ans, joined=joined)
    ans = digest_special(
        ans,
        long_enabled=long_enabled,
        short_enabled=short_enabled,
        is_posix=is_posix,
        reconciles_orders=reconciles_orders,
        special=special,
    )
    ans = digest_order(
        ans,
        long_enabled=long_enabled,
        short_enabled=short_enabled,
        is_posix=is_posix,
        reconciles_orders=reconciles_orders,
        special=special,
        longopts=longopts,
    )
    ans = digest_bundling(
        ans,
        bundling=bundling,
        long_enabled=long_enabled,
    )
    return ans


def digest_joined(items: list[Item], *, joined: Tuning) -> list[Item]:
    """Normalize the separation of option values without changing their content."""
    item: Item
    if joined == Tuning.MAINTAIN:
        return items
    for item in items:
        if isinstance(item, Option) and item.right is not None:
            item.joined = joined == Tuning.MAXIMIZE
    return items


def digest_abbr(
    items: list[Item],
    *,
    abbr: Tuning,
    longopts: tuple[str, ...] | None,
    short_enabled: bool,
) -> list[Item]:
    ans: list[Item]
    item: Item
    keys: list[str]
    option: str
    options: list[str]
    candidate: str
    length: int
    spec: str
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
            keys = [key for key in options if key.startswith(candidate)]
            if [item.fullkey] == keys:
                item.abbrlen = length
                break
    return ans


def digest_bundling(
    items: list[Item],
    *,
    bundling: Tuning,
    long_enabled: bool,
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
    """Combine short options without treating positional tokens as a hard barrier.

    Adjacent bundles are always combined when the earlier bundle has no
    argument.  A *single, isolated* short option can also join an earlier
    compatible bundle across intervening positionals.  A subsequent run of
    adjacent short options stays together rather than being moved across
    positionals when order reconciliation has not already done so.

    Never combine across a long option or a ``--`` delimiter, and never put
    another option after a bundle that carries an argument.
    """
    adjacent_bundle: Any
    candidate: int
    index: Any
    isolated_short_option: Any
    item: Any
    ans: list[Item]
    ans = []
    for index, item in enumerate(items):
        if not isinstance(item, Bundle):
            ans.append(item)
            continue

        candidate = len(ans) - 1
        adjacent_bundle = candidate >= 0 and isinstance(ans[candidate], Bundle)
        isolated_short_option = len(item.chars) == 1 and (
            index + 1 == len(items) or not isinstance(items[index + 1], Bundle)
        )
        if isolated_short_option and not adjacent_bundle:
            # A lone short option may join an earlier bundle across one or
            # more positional arguments.  Long options and ``--`` are barriers.
            while candidate >= 0 and isinstance(ans[candidate], Positional):
                candidate -= 1

        if (
            candidate >= 0
            and isinstance(ans[candidate], Bundle)
            and ans[candidate].right is None
        ):
            item.chars = ans[candidate].chars + item.chars
            ans[candidate] = item
        else:
            ans.append(item)
    return ans


def digest_order(
    items: list[Item],
    *,
    is_posix: bool,
    long_enabled: bool,
    longopts: tuple[str, ...] | None,
    reconciles_orders: bool,
    short_enabled: bool,
    special: Tuning,
) -> list[Item]:
    ans: list[Any]
    comp: bool
    index: int
    insert_at: Any
    ans = list(items)
    if not (long_enabled or short_enabled):
        return ans
    if not reconciles_orders:
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
        insert_at = index + 1
        if special == Tuning.MAINTAIN and isinstance(ans[-1], Positional):
            if ans[-1].value.split("=", 1)[0] in (
                digest_long_fullkey(spec, short_enabled=short_enabled)
                for spec in (longopts or ())
            ):
                if any(
                    isinstance(item, Positional) and item.value == "--"
                    for item in ans[index + 1 : -1]
                ):
                    if ans[index + 1].value != "-":
                        return ans
                else:
                    insert_at = len(ans) - 1
        ans.insert(insert_at, Special())
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
        return digest_special_max(
            items,
            insert_leading=kwargs["long_enabled"] or kwargs["short_enabled"],
        )
    return list(items)


def digest_special_max(
    items: list[Item], *, insert_leading: bool = True
) -> list[Item]:
    """Maximize the number of arguments following ``--``.

    Parsed options must remain before the delimiter, while positional items
    can be moved behind it.  Preserve the order within each group and retain
    the positional items that were already behind an existing delimiter.

    Unlike general order reconciliation, this grouping is part of the
    requested ``special=MAXIMIZE`` transformation, so it applies even when
    ``reconciles_orders`` is false.
    """
    found_special: Any
    item: Any
    ans: list[Item]
    ans = list(items)
    if not insert_leading:
        # With all option parsing disabled, ``--`` is not a delimiter.
        return ans

    options: list[Item]
    options = []
    positional: list[Item]
    positional = []
    trailing: list[Item]
    trailing = []
    found_special = False
    for item in ans:
        if found_special:
            trailing.append(item)
        elif isinstance(item, Special):
            found_special = True
        elif isinstance(item, Option):
            options.append(item)
        else:
            positional.append(item)

    # A required-value option at the end of the option section can consume
    # the literal "--"; a separate delimiter is then still necessary.
    if options and options[-1].ishungry():
        options[-1].joined = False
        options[-1].right = "--"

    return options + [Special()] + positional + trailing


def digest_special_min(
    items: list[Item],
    *,
    is_posix: bool,
    long_enabled: bool,
    reconciles_orders: bool,
    short_enabled: bool,
) -> list[Item]:
    ans: list[Any]
    index: int
    isdel: bool
    isposix: bool
    ans = list(items)
    isdel = True
    isposix = is_posix and not (
        reconciles_orders and (long_enabled or short_enabled)
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
    ans: str
    if short_enabled:
        ans = "--" + spec
    else:
        ans = "-" + spec
    if ans.endswith("=?"):
        return ans[:-2]
    if ans.endswith("="):
        return ans[:-1]
    return ans

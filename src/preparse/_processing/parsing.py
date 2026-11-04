__all__: list[str] = ["parse"]

import operator
from typing import Any

from preparse._items.Bundle import Bundle
from preparse._items.Item import Item
from preparse._items.Long import Long
from preparse._items.Option import Option
from preparse._items.Positional import Positional
from preparse._items.Special import Special
from preparse.abc.Message import Message
from preparse.messaging.AmbiguousOptionMessage import (
    AmbiguousOptionMessage as AOM,
)
from preparse.messaging.InvalidOptionMessage import InvalidOptionMessage as IOM
from preparse.messaging.RequiredArgumentMessage import (
    RequiredArgumentMessage as RAM,
)
from preparse.messaging.UnallowedArgumentMessage import (
    UnallowedArgumentMessage as UAM,
)
from preparse.namedtuple.Reserve import Reserve


def parse(
    items: list[str],
    *,
    is_posix: bool,
    longopts: tuple[str, ...] | None,
    reserve: Reserve | None,
    shortopts: str | None,
) -> tuple[list[Item], list[Message]]:
    broken: bool
    item: str
    last: Any
    messages: list[Message]
    preparsed: list[Item]
    messages = list()
    preparsed = list()
    broken = shortopts is None and longopts is None
    last = None
    for item in items:
        if broken:
            # if we are in the positional-only part
            preparsed.append(Positional(item))
            continue
        if last is not None:
            # if the last item hungers for a value
            last.right = item
            last.joined = False
            preparsed.append(last)
            last = None
            continue
        if item == "--":
            preparsed.append(Special())
            broken = True
            continue
        if Positional(item).isobvious():
            # if the item is positional
            preparsed.append(Positional(item))
            broken = is_posix
            continue
        last = parse_option(
            item,
            shortopts=shortopts,
            longopts=longopts,
            messages=messages,
        )
        if not last.ishungry():
            preparsed.append(last)
            last = None
    if last is None:
        return preparsed, messages
    # if the last item is starved
    if isinstance(last, Long):
        messages.append(RAM(option=last.fullkey, is_long=True))
    else:
        messages.append(RAM(option=last.chars[-1], is_long=False))
    if reserve is not None:
        last.joined, last.right = reserve
        preparsed.append(last)
    return preparsed, messages


def parse_bundling(
    arg: str,
    *,
    messages: list[Message],
    shortopts: str,
) -> Bundle:
    ans: Bundle
    x: int
    y: str
    mode: Any
    ans = Bundle(chars="", argmode="")
    for x, y in enumerate(arg):
        if x == 0:
            continue
        ans.chars += y
        mode = short_argmode(y, shortopts)
        if mode is None:
            messages.append(IOM(option=y, is_long=False))
            continue
        ans.argmode = mode
        if mode == "":
            continue
        if mode == "::" or x < len(arg) - 1:
            ans.joined = True
            ans.right = arg[x + 1 :]
        return ans
    return ans


def parse_is_long(
    arg: str,
    *,
    longopts: tuple[str, ...] | None,
    shortopts: str | None,
) -> bool:
    if longopts is not None and shortopts is not None:
        return arg.startswith("--")
    return shortopts is None


def short_argmode(option: str, shortopts: str) -> str | None:
    """Read a short-option spec: no suffix, :, or :: (optional)."""
    char: Any
    index: Any
    for index, char in enumerate(shortopts):
        if char == option and char != ":":
            if shortopts[index + 1 : index + 3] == "::":
                return "::"
            if shortopts[index + 1 : index + 2] == ":":
                return ":"
            return ""
    return None


def long_argmode(spec: str) -> tuple[str, str]:
    """Read a long-option spec: no suffix, =, or =? (optional)."""
    if spec.endswith("=?"):
        return spec[:-2], "::"
    if spec.endswith("="):
        return spec[:-1], ":"
    return spec, ""


def long_fullkey(spec: str, *, shortopts_allowed: bool) -> tuple[str, str]:
    """Apply the long-option prefix literally, after removing its nargs suffix."""
    key: Any
    mode: Any
    prefix: Any
    key, mode = long_argmode(spec)
    prefix = "--" if shortopts_allowed else "-"
    return prefix + key, mode


def parse_long(
    arg: str,
    *,
    longopts: tuple[str, ...],
    messages: list[Message],
    shortopts_allowed: bool,
) -> Long:
    ans: Long
    key: Any
    matches: Any
    message: Message
    options: list[tuple[str, str]]
    parts: list[str]
    parts = arg.split("=", 1)
    ans = Long(fullkey=parts.pop(0))
    if parts:
        ans.joined = True
        ans.right = parts.pop()
    ans.abbrlen = len(ans.fullkey)
    # Never normalize or remove leading dashes from the declared name.
    # Only the nargs suffix is removed; the prefix is always prepended.
    options = [
        long_fullkey(spec, shortopts_allowed=shortopts_allowed)
        for spec in longopts
    ]
    matches = [(key, mode) for key, mode in options if key == ans.fullkey]
    if matches:
        # getopt prefers an exact bare name over its argument variants.
        matches = [min(matches, key=operator.itemgetter(1))]
    else:
        matches = [
            (key, mode) for key, mode in options if key.startswith(ans.fullkey)
        ]
    if not matches:
        ans.argmode = "::"
        messages.append(IOM(option=arg, is_long=True))
        return ans
    if len(matches) >= 2:
        ans.argmode = "::"
        message = AOM(
            option=arg,
            possibilities=map(operator.itemgetter(0), matches),
        )
        messages.append(message)
        return ans
    key, ans.argmode = matches[0]
    ans.fullkey = key
    if ans.argmode == "" and ans.right is not None:
        messages.append(UAM(option=ans.fullkey))
    return ans


def parse_option(
    arg: str,
    *,
    longopts: tuple[str, ...] | None,
    messages: list[Message],
    shortopts: str | None,
) -> Option:
    if parse_is_long(arg, shortopts=shortopts, longopts=longopts):
        return parse_long(
            arg,
            messages=messages,
            longopts=longopts if longopts is not None else (),
            shortopts_allowed=shortopts is not None,
        )
    return parse_bundling(
        arg,
        messages=messages,
        shortopts=shortopts if shortopts is not None else "",
    )

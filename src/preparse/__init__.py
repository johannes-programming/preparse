from __future__ import annotations

__all__: list[str] = ["PreParser"]

import sys
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from enum import Enum, IntEnum
from typing import Any, Protocol, Self, overload, runtime_checkable


@runtime_checkable
class SupportsKeysAndGetitem[Key, Value](Protocol):
    def __getitem__(self: Self, key: Key, /) -> Value: ...
    def keys(self: Self, /) -> Iterable[Key]: ...


type OptDictOther[Key] = (
    SupportsKeysAndGetitem[Key, object] | Iterable[tuple[Key, object]] | None
)


@dataclass
class _Item:
    # A logical option, positional argument, or end-of-options marker.
    kind: str
    text: str = ""
    key: str | None = None
    nargs: int = 0
    value: str | None = None
    attached: bool = False
    group: int = -1
    # Invalid or ambiguous options are retained without speculative rewrites.
    locked: bool = False
    # A short option is a single character, even when it is '-'.
    character: str = ""
    # A required option with no available value.
    starved: bool = False


class PreParser:
    """Preparser and its three in-place mutable configuration objects."""

    class Message(ABC):
        """Abstract base of structured preparsing diagnostics."""

        @abstractmethod
        def oneliner(self: Self, /) -> str:
            """Return a one-line getopt-style description."""

    @dataclass(eq=True)
    class AmbiguousOptionMessage(Message):
        option: str
        possibilities: list[str]

        def oneliner(self: Self, /) -> str:
            ans: str
            ans = "option '%s' is ambiguous; possibilities:" % self.option
            for x in self.possibilities:
                ans += " '%s'" % x
            return ans

    @dataclass(eq=True)
    class InvalidOptionMessage(Message):
        option: str
        is_long: bool

        def oneliner(self: Self, /) -> str:
            return (
                "unrecognized option '%s'"
                if self.is_long
                else "invalid option -- '%s'"
            ) % self.option

    @dataclass(eq=True)
    class RequiredArgumentMessage(Message):
        option: str
        is_long: bool

        def oneliner(self: Self, /) -> str:
            return (
                "option '%s' requires an argument"
                if self.is_long
                else "option requires an argument -- '%s'"
            ) % self.option

    @dataclass(eq=True)
    class UnallowedArgumentMessage(Message):
        option: str

        def oneliner(self: Self, /) -> str:
            return "option '%s' doesn't allow an argument" % self.option

    class Framework:
        def __init__(
            self: Self,
            other: PreParser.Framework | None = None,
            /,
            *,
            allows_long: bool | None = None,
            allows_short: bool | None = None,
            is_posix: bool | None = None,
        ) -> None:
            self.allows_long = True
            self.allows_short = True
            self.is_posix = False
            self.update(other)
            self.update_fields(
                allows_long=allows_long,
                allows_short=allows_short,
                is_posix=is_posix,
            )

        def copy(self: Self, /) -> Self:
            return type(self)(self)

        def update(self: Self, other: PreParser.Framework | None) -> None:
            if other is not None:
                self.update_fields(
                    allows_long=other.allows_long,
                    allows_short=other.allows_short,
                    is_posix=other.is_posix,
                )

        def update_fields(
            self,
            *,
            allows_long: bool | None = None,
            allows_short: bool | None = None,
            is_posix: bool | None = None,
        ) -> None:
            if allows_long is not None:
                self.allows_long = allows_long
            if allows_short is not None:
                self.allows_short = allows_short
            if is_posix is not None:
                self.is_posix = is_posix

    class OptDict(dict[str, Any]):
        """A dictionary which normalizes keys and argument-count values."""

        class Nargs(IntEnum):
            NO_ARGUMENT = 0
            REQUIRED_ARGUMENT = 1
            OPTIONAL_ARGUMENT = 2

            @classmethod
            def _missing_(
                cls: type[Self], /, value: object
            ) -> PreParser.OptDict.Nargs:
                return cls(0) if value is None else cls(2)

        def __contains__(self: Self, key: object, /) -> bool:
            return dict.__contains__(self, str(key))

        def __delitem__(self: Self, key: object, /) -> None:
            dict.__delitem__(self, str(key))

        def __getitem__(self: Self, key: object, /) -> Nargs:
            return dict.__getitem__(self, str(key))

        def __init__[Key](
            self: Self,
            other: OptDictOther[Key] = None,
            /,
            **kwargs: object,
        ) -> None:
            super().__init__()
            self.update(other, **kwargs)

        def __ior__[Key](
            self: Self,
            other: OptDictOther[Key],
            /,
        ) -> Self:
            self.update(other)
            return self

        def __or__[Key](
            self: Self,
            other: OptDictOther[Key],
            /,
        ) -> Self:
            ans: Self
            ans = self.copy()
            ans.update(other)
            return ans

        def __repr__(self: Self, /) -> str:
            return f"{type(self).__name__}({dict(self)})"

        def __setitem__(self: Self, key: object, value: object, /) -> None:
            if value is None:
                return
            dict.__setitem__(self, str(key), self.Nargs(value))

        def copy(self: Self, /) -> Self:
            return type(self)(self)

        @classmethod
        def fromkeys(
            cls: type[Self],
            keys: Iterable[object],
            value: object = None,
            /,
        ) -> Self:
            ans: Self
            ans = cls()
            if value is None:
                return cls()
            for key in keys:
                ans[key] = value
            return ans

        @overload
        def get(
            self: Self, key: object, default: None = None, /
        ) -> Nargs | None: ...
        @overload
        def get[Value](
            self: Self, key: object, default: Value, /
        ) -> Nargs | Value: ...
        def get(self: Self, key: object, default: Any = None, /) -> Any:
            return dict.get(self, str(key), default)

        @overload
        def pop(self: Self, key: object, /) -> Nargs: ...
        @overload
        def pop[Value](
            self: Self, key: object, default: Value, /
        ) -> Nargs | Value: ...
        def pop(self: Self, key: object, /, *args: Any) -> Any:
            return dict.pop(self, str(key), *args)

        def setdefault(
            self: Self, key: object, default: object = None
        ) -> Nargs:
            key = str(key)
            if dict.__contains__(self, key):
                return dict.__getitem__(self, key)
            self[key] = default
            return dict.__getitem__(self, key)

        def update[Key](
            self: Self,
            other: OptDictOther[Key] = None,
            /,
            **kwargs: object,
        ) -> None:
            if other is not None and isinstance(other, SupportsKeysAndGetitem):
                for x in other.keys():
                    self[str(x)] = PreParser.OptDict.Nargs(other[x])
            elif other is not None:
                for x, y in other:
                    self[str(x)] = PreParser.OptDict.Nargs(y)
            for x, y in kwargs.items():
                self[str(x)] = PreParser.OptDict.Nargs(y)

    class Transformation:

        class Tuning(IntEnum):
            MINIMIZE = 0
            MAXIMIZE = 1
            MAINTAIN = 2

            @classmethod
            def _missing_(
                cls: type[Self], /, value: object
            ) -> PreParser.Transformation.Tuning:
                return cls(0) if value is None else cls(2)

        class Depletion(Enum):
            DROP_OPT = "DROP_OPT"
            DEFER = "DEFER"

        def __init__(
            self: Self,
            other: PreParser.Transformation | None = None,
            /,
            *,
            abbr: PreParser.Transformation.Tuning | None = None,
            bundling: PreParser.Transformation.Tuning | None = None,
            depletion: Depletion | str | None = None,
            equal: PreParser.Transformation.Tuning | None = None,
            order_compatibility: PreParser.Transformation.Tuning | None = None,
        ) -> None:
            self.order_compatibility = PreParser.Transformation.Tuning.MAXIMIZE
            self.bundling = PreParser.Transformation.Tuning.MAINTAIN
            self.abbr = PreParser.Transformation.Tuning.MINIMIZE
            self.equal = PreParser.Transformation.Tuning.MAINTAIN
            self.depletion = PreParser.Transformation.Depletion.DROP_OPT
            self.update(other)
            self.update_fields(
                order_compatibility=order_compatibility,
                bundling=bundling,
                abbr=abbr,
                equal=equal,
                depletion=depletion,
            )

        def copy(self: Self, /) -> Self:
            return type(self)(self)

        def update(
            self: Self, other: PreParser.Transformation | None = None, /
        ) -> None:
            if other is not None:
                self.update_fields(
                    order_compatibility=other.order_compatibility,
                    bundling=other.bundling,
                    abbr=other.abbr,
                    equal=other.equal,
                    depletion=other.depletion,
                )

        def update_fields(
            self,
            *,
            order_compatibility: Tuning | None = None,
            bundling: Tuning | None = None,
            abbr: Tuning | None = None,
            equal: Tuning | None = None,
            depletion: Depletion | str | None = None,
        ) -> None:
            for field, value in (
                ("order_compatibility", order_compatibility),
                ("bundling", bundling),
                ("abbr", abbr),
                ("equal", equal),
            ):
                if value is not None:
                    setattr(
                        self, field, PreParser.Transformation.Tuning(value)
                    )
            if depletion is not None:
                if not isinstance(
                    depletion, (PreParser.Transformation.Depletion, str)
                ):
                    raise TypeError(
                        "depletion must be a Depletion enum or a string"
                    )
                self.depletion = depletion

    def __init__[Key](
        self,
        other: PreParser | None = None,
        /,
        *,
        framework: Framework | None = None,
        optDict: (
            SupportsKeysAndGetitem[Key, object]
            | Iterable[tuple[Key, object]]
            | None
        ) = None,
        transformation: PreParser.Transformation | None = None,
    ) -> None:
        self._framework = PreParser.Framework()
        self._optDict = PreParser.OptDict()
        self._transformation = PreParser.Transformation()
        if other is not None:
            self.framework = other.framework
            self.optDict = other.optDict
            self.transformation = other.transformation
        if framework is not None:
            self.framework = framework
        if optDict is not None:
            self.optDict = optDict
        if transformation is not None:
            self.transformation = transformation

    def copy(self: Self, /) -> Self:
        return type(self)(self)

    @property
    def framework(self: Self, /) -> Framework:
        return self._framework

    @framework.setter
    def framework(self: Self, other: Framework | None, /) -> None:
        self._framework.update(other)

    @property
    def optDict(self: Self, /) -> OptDict:
        return self._optDict

    @optDict.setter
    def optDict[Key](
        self: Self,
        other: (
            SupportsKeysAndGetitem[Key, object]
            | Iterable[tuple[Key, object]]
            | None
        ),
        /,
    ) -> None:
        data: PreParser.OptDict
        if other is not None:
            data = PreParser.OptDict(other)
            self.optDict.clear()
            self.optDict.update(data)

    @property
    def transformation(self: Self, /) -> Transformation:
        return self._transformation

    @transformation.setter
    def transformation(self: Self, other: Transformation | None, /) -> None:
        self._transformation.update(other)

    def _definitions(
        self,
    ) -> tuple[dict[str, Nargs], dict[str, Nargs]]:
        """Return effective short and long options, in dictionary order."""
        shorts: dict[str, Nargs] = {}
        longs: dict[str, Nargs] = {}
        f = self.framework
        for key, value in self.optDict.items():
            if not key.startswith("-"):
                continue
            if f.allows_short and len(key) == 2 and not key.startswith("---"):
                shorts[key[1]] = value
            if f.allows_long:
                if f.allows_short:
                    if key.startswith("--") and len(key) > 2:
                        longs[key] = value
                else:
                    longs[key] = value
        return shorts, longs

    def _long_match(
        self, name: str, longs: Mapping[str, PreParser.OptDict.Nargs]
    ) -> tuple[str | None, list[str]]:
        # Exact spelling always takes precedence over any abbreviation.
        if name in longs:
            return name, []
        # The bare delimiter cannot serve as an abbreviation for a longer
        # long-option name, even if an equals sign follows it.
        if name == "--":
            return None, []
        # A spelling of '-=value' is a special way to use the '--' long
        # definition in long-only frameworks.
        if not self.framework.allows_short and name == "-" and "--" in longs:
            return "--", []
        # A one-dash and a two-dash dictionary key are *different* entries.
        # An abbreviation retains the spelling's leading-dash convention.
        n_dashes = len(name) - len(name.lstrip("-"))
        candidates = [
            k
            for k in longs
            if k.startswith(name) and (len(k) - len(k.lstrip("-"))) == n_dashes
        ]
        if len(candidates) == 1:
            return candidates[0], []
        if len(candidates) > 1:
            return None, candidates
        return None, []

    def _scan(
        self,
        arglist: list[str],
        *,
        posix: bool,
        report: bool = True,
    ) -> tuple[list[_Item], list[Message]]:
        """Perform getopt-like recognition without any goal-based rewrites."""
        shorts, longs = self._definitions()
        items: list[_Item] = []
        messages: list[PreParser.Message] = []
        i = 0
        stopped = False
        while i < len(arglist):
            token = arglist[i]
            group = i
            i += 1
            if stopped:
                items.append(_Item("pos", token, group=group))
                continue
            if token == "--":
                items.append(_Item("delimiter", "--", group=group))
                stopped = True
                continue
            if not token.startswith("-") or token == "-":
                items.append(_Item("pos", token, group=group))
                if posix:
                    stopped = True
                continue

            long_token = self.framework.allows_long and (
                not self.framework.allows_short or token.startswith("--")
            )
            if long_token:
                name, separator, value = token.partition("=")
                matched, ambiguous = self._long_match(name, longs)
                if ambiguous:
                    if report:
                        messages.append(
                            PreParser.AmbiguousOptionMessage(token, ambiguous)
                        )
                    items.append(
                        _Item(
                            "long",
                            name,
                            value=value if separator else None,
                            attached=bool(separator),
                            group=group,
                            locked=True,
                        )
                    )
                    continue
                if matched is None:
                    if report:
                        messages.append(
                            PreParser.InvalidOptionMessage(token, True)
                        )
                    items.append(
                        _Item(
                            "long",
                            name,
                            nargs=2,
                            value=value if separator else None,
                            attached=bool(separator),
                            group=group,
                            locked=True,
                        )
                    )
                    continue
                nargs = int(longs[matched])
                locked = False
                starved = False
                if separator and nargs == 0:
                    if report:
                        messages.append(
                            PreParser.UnallowedArgumentMessage(name)
                        )
                    locked = True
                elif not separator and nargs == 1:
                    if i < len(arglist):
                        value = arglist[i]
                        i += 1
                    else:
                        value = None
                        starved = True
                        if report:
                            messages.append(
                                PreParser.RequiredArgumentMessage(name, True)
                            )
                items.append(
                    _Item(
                        "long",
                        name,
                        key=matched,
                        nargs=nargs,
                        value=value if separator or nargs == 1 else None,
                        attached=bool(separator),
                        group=group,
                        locked=locked,
                        starved=starved,
                    )
                )
                continue

            # The remainder of this token is a cluster of short characters.
            # An argument-taking character consumes the rest of the cluster.
            rest = token[1:]
            p = 0
            while p < len(rest):
                char = rest[p]
                p += 1
                nargs = int(shorts[char]) if char in shorts else 0
                unknown = char not in shorts
                if unknown and report:
                    messages.append(
                        PreParser.InvalidOptionMessage(char, False)
                    )
                tail = rest[p:]
                value: str | None = None
                attached = False
                starved = False
                if nargs in (1, 2):
                    if tail:
                        value = tail
                        attached = True
                    elif nargs == 1:
                        if i < len(arglist):
                            value = arglist[i]
                            i += 1
                        else:
                            starved = True
                            if report:
                                messages.append(
                                    PreParser.RequiredArgumentMessage(
                                        char, False
                                    )
                                )
                    p = len(rest)
                items.append(
                    _Item(
                        "short",
                        "-" + char,
                        key="-" + char if not unknown else None,
                        nargs=nargs,
                        value=value,
                        attached=attached,
                        group=group,
                        locked=unknown,
                        character=char,
                        starved=starved,
                    )
                )
        return items, messages

    @staticmethod
    def _signature(items: list[_Item]) -> tuple:
        return tuple(
            (x.kind, x.key or x.text, x.value)
            for x in items
            if x.kind != "delimiter"
        )

    def _compatible(self, arglist: list[str]) -> bool:
        """Compare interpretations, ignoring only the delimiter's own token."""
        first, _ = self._scan(arglist, posix=True, report=False)
        second, _ = self._scan(arglist, posix=False, report=False)
        return self._signature(first) == self._signature(second)

    def _order(self, items: list[_Item], original: list[str]) -> list[_Item]:
        tuning = self.transformation.order_compatibility
        if tuning == PreParser.Transformation.Tuning.MAINTAIN:
            return items
        compatible = self._compatible(original)
        if tuning == PreParser.Transformation.Tuning.MINIMIZE:
            if not compatible:
                return items
            # Move an existing positional before an option, preserving the
            # relative order of all options and of all positionals.
            opt_indices = [
                i for i, x in enumerate(items) if x.kind in ("short", "long")
            ]
            pos_indices = [
                i
                for i, x in enumerate(items)
                if x.kind == "pos"
                and (not x.text.startswith("-") or x.text == "-")
            ]
            if not opt_indices:
                # An existing delimiter can also distinguish the two order
                # disciplines: once POSIX has seen a positional, it treats
                # a subsequent '--' as an ordinary positional token.
                boundary = next(
                    (i for i, x in enumerate(items) if x.kind == "delimiter"),
                    None,
                )
                if boundary is not None:
                    later = next(
                        (i for i in pos_indices if i > boundary), None
                    )
                    if later is not None:
                        moved = list(items)
                        positional = moved.pop(later)
                        moved.insert(boundary, positional)
                        return moved
                return items
            if not pos_indices:
                return items
            option_index = opt_indices[-1]
            # Do not insert between characters from the same short bundle.
            # A split there could turn the short character '-' into the
            # standalone delimiter '--'.
            if items[option_index].kind == "short":
                group = items[option_index].group
                while (
                    option_index > 0
                    and items[option_index - 1].kind == "short"
                    and items[option_index - 1].group == group
                ):
                    option_index -= 1
            candidates = [j for j in pos_indices if j > opt_indices[-1]]
            if not candidates:
                return items
            moved = list(items)
            positional = moved.pop(candidates[0])
            moved.insert(option_index, positional)
            return moved

        # MAXIMIZE: move recognized options before positionals, leaving the
        # relative order within each category unchanged. A delimiter retains
        # the boundary between token regions.
        if compatible:
            return items
        if self.framework.is_posix:
            # POSIX may already have treated later option-looking strings as
            # positional. Introduce an end marker so non-POSIX does likewise.
            before = next(
                (i for i, x in enumerate(items) if x.kind == "pos"), None
            )
            if before is not None:
                return (
                    items[:before]
                    + [_Item("delimiter", "--")]
                    + items[before:]
                )
            return items
        # Non-POSIX recognizes all options preceding an explicit delimiter.
        first_delim = next(
            (i for i, x in enumerate(items) if x.kind == "delimiter"),
            len(items),
        )
        leading, trailing = items[:first_delim], items[first_delim:]
        options = [x for x in leading if x.kind in ("short", "long")]
        positions = [x for x in leading if x.kind == "pos"]
        if (
            options
            and options[-1].starved
            and self.transformation.depletion
            is PreParser.Transformation.Depletion.DEFER
        ):
            # DEFER expressly keeps an unfulfilled required option at the
            # end. Moving it in front of a positional would *consume* that
            # positional and cease to defer the option.
            return options[:-1] + positions + options[-1:] + trailing
        if trailing and positions:
            # A marker after a positional is invisible to POSIX recognition.
            # Place the *existing* marker before all positionals instead.
            return options + trailing[:1] + positions + trailing[1:]
        return options + positions + trailing

    def _abbreviation(
        self, item: _Item, longs: Mapping[str, PreParser.OptDict.Nargs]
    ) -> str:
        if item.key is None or item.locked:
            return item.text
        tuning = self.transformation.abbr
        if tuning == PreParser.Transformation.Tuning.MAINTAIN:
            return item.text
        if tuning == PreParser.Transformation.Tuning.MAXIMIZE:
            return item.key
        # Find the shortest abbreviation *resolving to this same definition*.
        # Prefixes '-' and '--' are reserved as positional/delimiter tokens.
        key = item.key
        minimum = 3 if key.startswith("--") else 2
        for end in range(minimum, len(key) + 1):
            candidate = key[:end]
            found, ambiguous = self._long_match(candidate, longs)
            if found == key and not ambiguous:
                return candidate
        return item.text

    def _apply_depletion(self, items: list[_Item]) -> list[_Item]:
        result = []
        for x in items:
            if x.starved:
                depletion = self.transformation.depletion
                if depletion is PreParser.Transformation.Depletion.DROP_OPT:
                    continue
                if depletion is PreParser.Transformation.Depletion.DEFER:
                    result.append(x)
                    continue
                x = replace(x, value=depletion, starved=False, attached=False)
            result.append(x)
        return result

    def _long_tokens(
        self, item: _Item, longs: Mapping[str, PreParser.OptDict.Nargs]
    ) -> list[str]:
        name = self._abbreviation(item, longs)
        if item.locked:
            return [name + ("=" + item.value if item.attached else "")]
        if item.value is None:
            return [name]
        if item.nargs == 2:
            # Optional long arguments can only be consumed when attached.
            return [name + "=" + item.value] if item.attached else [name]
        if item.nargs == 0:
            return [name + "=" + item.value] if item.attached else [name]
        equal = self.transformation.equal
        if equal == PreParser.Transformation.Tuning.MAXIMIZE:
            attach = True
        elif equal == PreParser.Transformation.Tuning.MINIMIZE:
            attach = False
        else:
            attach = item.attached
        if name in ("-", "--"):
            attach = True
        if attach:
            return [name + "=" + item.value]
        return [name, item.value]

    def _emit_shorts(self, items: list[_Item]) -> list[str]:
        """Serialize a run of short options without changing their meaning."""
        if not items:
            return []
        tuning = self.transformation.bundling
        if tuning == PreParser.Transformation.Tuning.MAXIMIZE:
            runs: list[list[_Item]] = []
            current: list[_Item] = []
            for x in items:
                if current and current[-1].nargs != 0:
                    runs.append(current)
                    current = []
                current.append(x)
                if x.nargs != 0:
                    runs.append(current)
                    current = []
            if current:
                runs.append(current)
        elif tuning == PreParser.Transformation.Tuning.MAINTAIN:
            runs = []
            current = []
            for x in items:
                if current and (
                    current[-1].group != x.group or current[-1].nargs != 0
                ):
                    runs.append(current)
                    current = []
                current.append(x)
                if x.nargs != 0:
                    runs.append(current)
                    current = []
            if current:
                runs.append(current)
        else:
            runs = [[x] for x in items]
            # A literal short character '-' cannot be emitted by itself:
            # '--' would end option processing. Keep it together with an
            # adjacent short character wherever that is semantically legal.
            j = 0
            while j < len(runs):
                if len(runs[j]) == 1 and runs[j][0].character == "-":
                    if j and runs[j - 1][-1].nargs == 0:
                        runs[j - 1].extend(runs.pop(j))
                        continue
                    if j + 1 < len(runs) and not self.framework.allows_long:
                        runs[j].extend(runs.pop(j + 1))
                j += 1

        result: list[str] = []
        for run in runs:
            chars = "".join(x.character for x in run)
            token = "-" + chars
            # With long options, anything beginning '--' is not a cluster.
            safe = token not in ("-", "--") and not (
                self.framework.allows_long and token.startswith("--")
            )
            if not safe:
                # Reproduce original grouping when splitting/rebundling is
                # impossible. This is particularly important for '-' options.
                groups: dict[int, list[_Item]] = {}
                for x in run:
                    groups.setdefault(x.group, []).append(x)
                if len(groups) > 1:
                    for group_items in groups.values():
                        result.extend(
                            self._emit_shorts_unmodified(group_items)
                        )
                    continue
                result.extend(self._emit_shorts_unmodified(run))
                continue
            last = run[-1]
            if last.nargs != 0 and last.value is not None and last.attached:
                token += last.value
                result.append(token)
            elif last.nargs != 0 and last.value is not None:
                result.extend((token, last.value))
            else:
                result.append(token)
        return result

    @staticmethod
    def _emit_shorts_unmodified(items: list[_Item]) -> list[str]:
        if not items:
            return []
        token = "-" + "".join(x.character for x in items)
        last = items[-1]
        if last.nargs != 0 and last.value is not None:
            return (
                [token + last.value] if last.attached else [token, last.value]
            )
        return [token]

    def _finish_bundling_block(
        self, block: list[_Item], result: list[_Item]
    ) -> None:
        if not block:
            return
        shorts = [x for x in block if x.kind == "short"]
        positions = [x for x in block if x.kind == "pos"]
        if len(shorts) >= 2 and positions:
            # More than one short character can safely form a cluster.
            token = "-" + "".join(x.character for x in shorts)
            if token != "--" and not (
                self.framework.allows_long and token.startswith("--")
            ):
                result.extend(shorts)
                result.extend(positions)
            else:
                result.extend(block)
        else:
            result.extend(block)
        block.clear()

    def _pack_for_bundling(self, items: list[_Item]) -> list[_Item]:
        """Bring combinable shorts together across insignificant positionals.

        Non-POSIX argument order permits positional/option interleaving. A
        bundling request may exploit that freedom even if order compatibility
        was otherwise set to MAINTAIN. In MINIMIZE compatibility mode, do not
        undo the deliberate positional/option separation.
        """
        if (
            self.transformation.bundling
            != PreParser.Transformation.Tuning.MAXIMIZE
            or self.framework.is_posix
            or self.transformation.order_compatibility
            == PreParser.Transformation.Tuning.MINIMIZE
        ):
            return items
        result: list[_Item] = []
        block: list[_Item] = []

        for x in items:
            if x.kind in ("long", "delimiter"):
                self._finish_bundling_block(block, result)
                result.append(x)
            else:
                block.append(x)
                if x.kind == "short" and x.nargs != 0:
                    self._finish_bundling_block(block, result)
        self._finish_bundling_block(block, result)
        return result

    def _serialize(self, items: list[_Item]) -> list[str]:
        _, longs = self._definitions()
        result: list[str] = []
        i = 0
        while i < len(items):
            x = items[i]
            if x.kind == "short":
                j = i + 1
                while j < len(items) and items[j].kind == "short":
                    # Do not carry a short-option argument across a boundary.
                    if items[j - 1].nargs != 0:
                        break
                    j += 1
                result.extend(self._emit_shorts(items[i:j]))
                i = j
                continue
            if x.kind == "long":
                result.extend(self._long_tokens(x, longs))
            elif x.kind == "pos":
                result.append(x.text)
            else:
                result.append("--")
            i += 1
        return result

    def parse_args(
        self, args: Iterable[str] | None = None
    ) -> tuple[list[str], list[Message]]:
        if args is None:
            arglist = sys.argv[1:]
        else:
            arglist = list(args)

        if not self.framework.allows_long and not self.framework.allows_short:
            return arglist, []

        items, messages = self._scan(arglist, posix=self.framework.is_posix)
        seen: set[tuple[str, ...]] = set()
        current = arglist
        # Transform to a fixed point, not just once: deleting a depleted
        # option or changing its position can expose a new opportunity for
        # order/equal normalization. Diagnostics always describe the input.
        for _ in range(32):
            state = tuple(current)
            if state in seen:
                break
            seen.add(state)
            if current is not arglist:
                items, _ = self._scan(
                    current, posix=self.framework.is_posix, report=False
                )
            processed = self._order(self._apply_depletion(items), current)
            transformed = self._serialize(self._pack_for_bundling(processed))
            if transformed == current:
                return transformed, messages
            current = transformed
        return current, messages

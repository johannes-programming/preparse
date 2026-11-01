"""A configurable argument preparser (not an application argument parser).

The scanner constructs option/positional events; rewriting takes place only
*after* each option's argument has been consumed. This prevents a rewrite from
accidentally causing an option's original value to be parsed as a new option.
"""

from __future__ import annotations

__all__: list[str] = ["PreParser"]
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable, Self

from preparse.abc.Copyable import Copyable
from preparse.abc.Message import Message
from preparse.enum.Depletion import Depletion
from preparse.enum.Nargs import Nargs
from preparse.enum.Tuning import Tuning
from preparse.messaging.AmbiguousOptionMessage import AmbiguousOptionMessage
from preparse.messaging.InvalidOptionMessage import InvalidOptionMessage
from preparse.messaging.RequiredArgumentMessage import RequiredArgumentMessage
from preparse.messaging.UnallowedArgumentMessage import (
    UnallowedArgumentMessage,
)

if TYPE_CHECKING:
    from preparse.core.Framework import Framework
    from preparse.core.OptList import OptList
    from preparse.core.Transformation import Transformation


@dataclass
class _Option:
    kind: str  # "short" or "long"
    spelling: str  # short char, or full hyphen-prefixed long spelling
    nargs: Nargs
    group: int  # input-token identifier (for preserving short bundling)
    arg: str | None = None
    attached: bool = False
    definition: int | None = None  # index in OptList, if uniquely recognized
    starved: bool = False


@dataclass
class _Positional:
    text: str


@dataclass
class _Delimiter:
    pass


_Event = _Option | _Positional | _Delimiter


class PreParser(Copyable):
    __slots__ = ("_framework", "_optList", "_transformation")

    def __init__(
        self,
        other: PreParser | None = None,
        /,
        *,
        framework: Framework | None = None,
        optList: OptList | None = None,
        transformation: Transformation | None = None,
    ) -> None:
        from .Framework import Framework
        from .OptList import OptList
        from .Transformation import Transformation

        self._framework = Framework()
        self._optList = OptList()
        self._transformation = Transformation()
        if other is not None:
            self.framework = other.framework
            self.optList = other.optList
            self.transformation = other.transformation
        self.framework = framework
        self.optList = optList
        self.transformation = transformation

    @property
    def framework(self: Self, /) -> Framework:
        return self._framework

    @framework.setter
    def framework(self: Self, value: Framework | None, /) -> None:
        if value is self._framework:
            return
        if value is not None:
            self._framework.__init__(value)

    @property
    def optList(self: Self, /) -> OptList:
        return self._optList

    @optList.setter
    def optList(self, value: Iterable[tuple[object, object]] | None) -> None:
        if value is None:
            return
        # Snapshot first, since an assignment may refer to self.optList or fail conversion.
        items = [(str(x), Nargs(y)) for x, y in value]
        self._optList.clear()
        self._optList.extend(items)

    @property
    def transformation(self) -> Transformation:
        return self._transformation

    @transformation.setter
    def transformation(self, value: Transformation | None) -> None:
        if value is self._transformation:
            return
        if value is not None:
            self._transformation.__init__(value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PreParser) and (
            self.framework == other.framework
            and self.optList == other.optList
            and self.transformation == other.transformation
        )

    def __repr__(self) -> str:
        return (
            f"PreParser(framework={self.framework!r}, "
            f"optList={self.optList!r}, transformation={self.transformation!r})"
        )

    def _dict(self: Self, /) -> dict[str, Any]:
        return dict(
            framework=self.framework,
            optList=self.optList,
            transformation=self.transformation,
        )

    def _long_definitions(self) -> list[tuple[int, str, str, Nargs]]:
        """Return (index, original key, name without prefix, nargs)."""
        ans: list[tuple[int, str, str, Nargs]] = []
        f = self.framework
        if not f.allows_long:
            return ans
        for index, (key, nargs) in enumerate(self.optList):
            if f.allows_short:
                if key.startswith("--") and len(key) > 2:
                    ans.append((index, key, key[2:], nargs))
            elif key.startswith("-"):
                # In long-only mode both one- and two-hyphen definitions
                # are effective, including an empty name (the "--" key).
                prefix = 2 if key.startswith("--") else 1
                ans.append((index, key, key[prefix:], nargs))
        return ans

    @staticmethod
    def _match_long(
        name: str,
        definitions: list[tuple[int, str, str, Nargs]],
    ) -> tuple[int | None, list[tuple[int, str, str, Nargs]]]:
        # An empty name is a valid exact name only when an actual option
        # defines it; it is not an abbreviation of every long option.
        if name == "":
            empty = [entry for entry in definitions if entry[2] == ""]
            return (empty[0][0], []) if empty else (None, [])
        matches = [entry for entry in definitions if entry[2].startswith(name)]
        exact = [entry for entry in matches if entry[2] == name]
        if exact:
            # Exact matches take precedence over abbreviations. If there
            # are duplicate normalized names, the earlier entry wins.
            return exact[0][0], []
        if len(matches) == 1:
            return matches[0][0], []
        if len(matches) > 1:
            return None, matches
        return None, []

    def _scan(self, arglist: list[str]) -> tuple[list[_Event], list[Message]]:
        events: list[_Event] = []
        messages: list[Message] = []
        f = self.framework
        short_definitions: dict[str, Nargs] = {}
        for key, nargs in self.optList:
            if f.allows_short and len(key) == 2 and key.startswith("-"):
                short_definitions[key[1]] = nargs
        long_definitions = self._long_definitions()
        by_index = {
            index: (key, name, nargs)
            for index, key, name, nargs in long_definitions
        }
        stop = False
        i = 0
        while i < len(arglist):
            word = arglist[i]
            group = i
            i += 1
            if stop:
                events.append(_Positional(word))
                continue
            if word == "--":
                events.append(_Delimiter())
                stop = True
                continue
            if word == "-" or not word.startswith("-"):
                events.append(_Positional(word))
                if f.is_posix:
                    stop = True
                continue

            is_long = f.allows_long and (
                not f.allows_short or word.startswith("--")
            )
            if is_long:
                # Both -name and --name are accepted with long-only parsing.
                hyphens = "--" if word.startswith("--") else "-"
                name_value = word[len(hyphens) :]
                name, equals, attached_value = name_value.partition("=")
                spelling = hyphens + name
                index, ambiguous = self._match_long(name, long_definitions)
                if ambiguous:
                    messages.append(
                        AmbiguousOptionMessage(
                            option=spelling,
                            possibilities=[entry[1] for entry in ambiguous],
                        )
                    )
                    events.append(
                        _Option(
                            "long",
                            spelling,
                            Nargs.OPTIONAL_ARGUMENT,
                            group,
                            attached_value if equals else None,
                            bool(equals),
                        )
                    )
                    continue
                if index is None:
                    messages.append(
                        InvalidOptionMessage(option=word, is_long=True)
                    )
                    events.append(
                        _Option(
                            "long",
                            spelling,
                            Nargs.OPTIONAL_ARGUMENT,
                            group,
                            attached_value if equals else None,
                            bool(equals),
                        )
                    )
                    continue
                key, defined_name, nargs = by_index[index]
                option = _Option(
                    "long", spelling, nargs, group, definition=index
                )
                if equals:
                    option.arg = attached_value
                    option.attached = True
                    if nargs == Nargs.NO_ARGUMENT:
                        messages.append(
                            UnallowedArgumentMessage(option=spelling)
                        )
                elif nargs == Nargs.REQUIRED_ARGUMENT:
                    if i < len(arglist):
                        option.arg = arglist[i]
                        i += 1
                    else:
                        option.starved = True
                        messages.append(
                            RequiredArgumentMessage(
                                option=spelling, is_long=True
                            )
                        )
                events.append(option)
                continue

            if f.allows_short:
                # This includes --foo in a short-only framework (as a
                # bundle starting with the short character '-').
                chars = word[1:]
                j = 0
                while j < len(chars):
                    char = chars[j]
                    j += 1
                    nargs = short_definitions.get(char)
                    if nargs is None:
                        nargs = Nargs.NO_ARGUMENT
                        messages.append(
                            InvalidOptionMessage(option=char, is_long=False)
                        )
                    option = _Option("short", char, nargs, group)
                    if j < len(chars) and nargs != Nargs.NO_ARGUMENT:
                        option.arg = chars[j:]
                        option.attached = True
                        j = len(chars)
                    elif nargs == Nargs.REQUIRED_ARGUMENT:
                        if i < len(arglist):
                            option.arg = arglist[i]
                            i += 1
                        else:
                            option.starved = True
                            messages.append(
                                RequiredArgumentMessage(
                                    option=char, is_long=False
                                )
                            )
                    events.append(option)
                continue
            # Unreachable when neither option type is enabled (early return).
            events.append(_Positional(word))
        return events, messages

    def _rewrite_long_names(self, events: list[_Event]) -> None:
        tuning = self.transformation.abbr
        if tuning == Tuning.MAINTAIN:
            return
        definitions = self._long_definitions()
        names = {index: name for index, _key, name, _nargs in definitions}
        for event in events:
            if not isinstance(event, _Option) or event.kind != "long":
                continue
            if event.definition is None:
                continue
            full = names.get(event.definition)
            if full is None:
                continue
            prefix = "--" if event.spelling.startswith("--") else "-"
            # Empty names must keep their '=' form, if present.
            if tuning == Tuning.MINIMIZE:
                new_name = full
            else:
                new_name = full
                for length in range(len(full) + 1):
                    candidate = full[:length]
                    spelling = prefix + candidate
                    # A bare '-' is positional; a bare '--' is a delimiter.
                    # An equals form of either spelling can nevertheless
                    # denote an empty-name long option in long-only mode.
                    if spelling in ("-", "--") and not event.attached:
                        continue
                    # If the name begins with '-', adding it to a one-hyphen
                    # prefix may instead create a two-hyphen token. Check
                    # what the scanner will actually see on the next parse.
                    actual_prefix = "--" if spelling.startswith("--") else "-"
                    physical_name = spelling[len(actual_prefix) :]
                    found, ambiguous = self._match_long(
                        physical_name, definitions
                    )
                    if found == event.definition and not ambiguous:
                        new_name = candidate
                        break
            event.spelling = prefix + new_name

    def _rewrite_separation(self, events: list[_Event]) -> None:
        tuning = self.transformation.separate
        if tuning == Tuning.MAINTAIN:
            return
        for event in events:
            if not isinstance(event, _Option):
                continue
            if event.arg is None or event.nargs != Nargs.REQUIRED_ARGUMENT:
                continue
            if tuning == Tuning.MAXIMIZE:
                # A bare '-' or '--' would not denote an empty-name long
                # option; its equals form must be retained.
                if event.kind == "long" and event.spelling in ("-", "--"):
                    continue
                if event.kind == "short" and event.spelling == "-":
                    continue
                event.attached = False
            elif tuning == Tuning.MINIMIZE:
                # A required short option with an empty attached argument
                # would become starved on the next parse.
                if event.kind == "short" and event.arg == "":
                    continue
                event.attached = True

    @staticmethod
    def _short_can_precede(option: _Option) -> bool:
        # Even an optional short with no attached value would swallow the
        # following characters as its optional value upon bundling.
        return option.nargs == Nargs.NO_ARGUMENT

    def _short_groups(self, options: list[_Option]) -> list[list[_Option]]:
        tuning = self.transformation.bundling
        groups: list[list[_Option]] = []
        for option in options:
            if not groups:
                groups.append([option])
                continue
            previous = groups[-1][-1]
            if tuning == Tuning.MAXIMIZE:
                combine = self._short_can_precede(previous)
            elif tuning == Tuning.MAINTAIN:
                combine = (
                    previous.group == option.group
                    and self._short_can_precede(previous)
                )
            else:
                combine = False
            if combine:
                groups[-1].append(option)
            else:
                groups.append([option])

        if tuning == Tuning.MINIMIZE:
            # The short-option character '-' cannot stand alone: '--' is
            # always the special delimiter. In short-only mode group it
            # with the following character (e.g. '-a-b' => '-a', '--b').
            # In both-option mode it must remain with the preceding short.
            ix = 0
            while ix < len(groups):
                group = groups[ix]
                if group[0].spelling == "-" and len(group) == 1:
                    if (
                        not self.framework.allows_long
                        and ix + 1 < len(groups)
                        and self._short_can_precede(group[-1])
                    ):
                        # Merging here is valid only if the two events
                        # came from the same input bundle.
                        if group[-1].group == groups[ix + 1][0].group:
                            group.extend(groups.pop(ix + 1))
                    elif ix > 0 and groups[ix - 1][-1].group == group[0].group:
                        if self._short_can_precede(groups[ix - 1][-1]):
                            groups[ix - 1].extend(groups.pop(ix))
                            continue
                ix += 1
        return groups

    def _render(self, events: list[_Event]) -> list[str]:
        result: list[str] = []
        i = 0
        while i < len(events):
            event = events[i]
            if isinstance(event, _Delimiter):
                result.append("--")
                i += 1
            elif isinstance(event, _Positional):
                result.append(event.text)
                i += 1
            elif event.kind == "long":
                text = event.spelling
                if event.arg is not None and event.attached:
                    text += "=" + event.arg
                result.append(text)
                if event.arg is not None and not event.attached:
                    result.append(event.arg)
                i += 1
            else:
                run: list[_Option] = []
                while i < len(events):
                    candidate = events[i]
                    if (
                        not isinstance(candidate, _Option)
                        or candidate.kind != "short"
                    ):
                        break
                    run.append(candidate)
                    i += 1
                for group in self._short_groups(run):
                    text = "-" + "".join(item.spelling for item in group)
                    tail = group[-1]
                    if tail.arg is not None and tail.attached:
                        text += tail.arg
                    result.append(text)
                    if tail.arg is not None and not tail.attached:
                        result.append(tail.arg)
        return result

    def _reconcile_order(self, events: list[_Event]) -> list[_Event]:
        if not self.transformation.reconciles_orders:
            return events
        if self.framework.is_posix:
            # POSIX parsing may have stopped at a positional token, leaving
            # option-shaped input tokens to be treated as literal values.
            # Shield these from non-POSIX parsing, too.
            if not any(isinstance(x, _Delimiter) for x in events):
                first_pos = next(
                    (
                        i
                        for i, x in enumerate(events)
                        if isinstance(x, _Positional)
                    ),
                    None,
                )
                if first_pos is not None:
                    tail = events[first_pos:]
                    if any(
                        isinstance(x, _Positional)
                        and x.text.startswith("-")
                        and x.text != "-"
                        for x in tail
                    ):
                        events = [*events[:first_pos], _Delimiter(), *tail]
            return events

        # A starved required option must remain the final input token.
        # Moving it ahead of a positional would give it that positional as
        # a value, changing the interpretation instead of reconciling it.
        if any(isinstance(x, _Option) and x.starved for x in events):
            return events
        # In non-POSIX mode, move complete option/value events ahead of the
        # positional arguments, without reaching across an explicit '--'.
        stop = next(
            (i for i, x in enumerate(events) if isinstance(x, _Delimiter)),
            len(events),
        )
        before = events[:stop]
        options = [x for x in before if isinstance(x, _Option)]
        positionals = [x for x in before if not isinstance(x, _Option)]
        return [*options, *positionals, *events[stop:]]

    def _rewrite_special(self, events: list[_Event]) -> list[_Event]:
        tuning = self.transformation.special
        if tuning == Tuning.MAINTAIN:
            return events
        delimiter_index = next(
            (i for i, x in enumerate(events) if isinstance(x, _Delimiter)),
            None,
        )
        if tuning == Tuning.MINIMIZE:
            if delimiter_index is None:
                return events
            # The delimiter can disappear only when all following tokens
            # would still be positional, including in non-POSIX order.
            after = events[delimiter_index + 1 :]
            if any(isinstance(x, _Option) for x in after):
                return events
            if any(
                isinstance(x, _Positional)
                and x.text.startswith("-")
                and x.text != "-"
                for x in after
            ):
                return events
            # If the POSIX/non-POSIX goal needs the delimiter, don't remove it.
            before = events[:delimiter_index]
            if (
                self.transformation.reconciles_orders
                and self.framework.is_posix
                and any(isinstance(x, _Positional) for x in before)
                and any(
                    isinstance(x, _Positional) and x.text.startswith("-")
                    for x in after
                )
            ):
                return events
            return [*events[:delimiter_index], *after]

        # A deferred, starved required option cannot be followed by a new
        # '--': getopt would consume the delimiter as the missing value.
        if any(isinstance(x, _Option) and x.starved for x in events):
            return events
        # MAXIMIZE special length: position '--' immediately after the last
        # actual option event (or at the beginning if there are no options).
        if delimiter_index is None:
            last = max(
                (i for i, x in enumerate(events) if isinstance(x, _Option)),
                default=-1,
            )
            return [*events[: last + 1], _Delimiter(), *events[last + 1 :]]
        before = events[:delimiter_index]
        last = max(
            (i for i, x in enumerate(before) if isinstance(x, _Option)),
            default=-1,
        )
        return [
            *before[: last + 1],
            _Delimiter(),
            *before[last + 1 :],
            *events[delimiter_index + 1 :],
        ]

    def parse_args(
        self: Self,
        /,
        args: Iterable[str] | None = None,
    ) -> tuple[list[str], list[Message]]:
        if args is None:
            arglist = sys.argv[1:]
        else:
            arglist = [str(x) for x in args]

        if not (self.framework.allows_long or self.framework.allows_short):
            return arglist, []

        result, messages = self._parse_once(arglist)
        if result == arglist:
            return result, messages

        # Rewrites can expose a second opportunity to fulfill another goal
        # (e.g. combining short tokens that previously belonged to separate
        # groups). Normalize to a stable representation so a second public
        # call cannot change the output. If goals fundamentally conflict and
        # cycle, preserve the input rather than claim the conflict is solved.
        seen = {tuple(arglist)}
        current = result
        for _ in range(24):
            state = tuple(current)
            if state in seen:
                return arglist, messages
            seen.add(state)
            next_result, _ = self._parse_once(current)
            if next_result == current:
                return current, messages
            current = next_result
        return arglist, messages

    def _parse_once(
        self, arglist: list[str]
    ) -> tuple[list[str], list[Message]]:
        events, messages = self._scan(arglist)
        modified: list[_Event] = []
        for event in events:
            if not isinstance(event, _Option) or not event.starved:
                modified.append(event)
                continue
            depletion = self.transformation.depletion
            if depletion == Depletion.DROP_OPT:
                # A short '-' cannot be emitted as a bare '--' (delimiter).
                # If dropping this option would strand a preceding bundled
                # '-', preserve the original group instead.
                if (
                    modified
                    and event.kind == "short"
                    and isinstance(modified[-1], _Option)
                    and modified[-1].kind == "short"
                    and modified[-1].spelling == "-"
                    and modified[-1].group == event.group
                    and sum(
                        isinstance(x, _Option) and x.group == event.group
                        for x in modified
                    )
                    == 1
                ):
                    modified.append(event)
                continue
            if isinstance(depletion, tuple):
                event.arg = depletion[1]
                event.attached = not depletion[0]
                # An empty attached value on a short option is not
                # representable: '-f' alone is a starved option.
                if event.kind == "short" and event.arg == "":
                    event.attached = False
                event.starved = False
            modified.append(event)

        events = self._reconcile_order(modified)
        self._rewrite_separation(events)
        self._rewrite_long_names(events)
        events = self._rewrite_special(events)
        return self._render(events), messages

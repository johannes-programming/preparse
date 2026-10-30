from __future__ import annotations

__all__: list[str] = ["OptDictOther"]

from collections.abc import Iterable

from preparse.typing.SupportsKeysAndGetitem import SupportsKeysAndGetitem

type OptDictOther[Key] = (
    SupportsKeysAndGetitem[Key, object] | Iterable[tuple[Key, object]] | None
)

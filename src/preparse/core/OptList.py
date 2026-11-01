"""A last-definition-wins, ordered option list."""

__all__: list[str] = [
    "OptList",
]

from collections.abc import Iterable
from typing import Any, Self

from preparse.abc.Copyable import Copyable
from preparse.enum.Nargs import Nargs


class OptList(list[tuple[str, Nargs]], Copyable):
    def __init__(
        self, other: Iterable[tuple[object, object]] | None = None, /
    ) -> None:
        super().__init__()
        if other is not None:
            self.extend(other)

    @staticmethod
    def _coerce(item: tuple[object, object]) -> tuple[str, Nargs]:
        key, value = item
        return str(key), Nargs(value)

    def _replace(self, items: Iterable[tuple[str, Nargs]]) -> None:
        sequence = list(items)
        seen: set[str] = set()
        unique: list[tuple[str, Nargs]] = []
        for key, value in reversed(sequence):
            if key not in seen:
                seen.add(key)
                unique.append((key, value))
        list.__setitem__(self, slice(None), reversed(unique))

    def append(self, item: tuple[object, object]) -> None:
        self._replace([*self, self._coerce(item)])

    def extend(self, iterable: Iterable[tuple[object, object]]) -> None:
        self._replace([*self, *(self._coerce(item) for item in iterable)])

    def insert(self, index: int, item: tuple[object, object]) -> None:
        items = list(self)
        items.insert(index, self._coerce(item))
        self._replace(items)

    def __setitem__(self, index: int | slice, item: Any) -> None:
        items = list(self)
        if isinstance(index, slice):
            items[index] = [self._coerce(x) for x in item]
        else:
            items[index] = self._coerce(item)
        self._replace(items)

    def __iadd__(self, iterable: Iterable[tuple[object, object]]) -> Self:
        self.extend(iterable)
        return self

    def __add__(self, iterable: list[tuple[str, Nargs]]) -> Self:
        result = self.copy()
        result.extend(iterable)
        return result

    def __mul__(self, count: int) -> Self:
        result = self.copy()
        result *= count
        return result

    __rmul__ = __mul__

    def __imul__(self, count: int) -> Self:
        self._replace(list(self) * count)
        return self

    def contains_key(self, key: object, /) -> bool:
        name = str(key)
        return any(k == name for k, _ in self)

    def del_by_key(self, key: object, /) -> None:
        name = str(key)
        for i, (k, _) in enumerate(self):
            if k == name:
                del self[i]
                return

    def get_by_key(self, key: object, default: Any = None, /) -> Any:
        name = str(key)
        for k, value in self:
            if k == name:
                return value
        return default

    def pop_by_key(self, key: object, default: Any = None, /) -> Any:
        name = str(key)
        for i, (k, value) in enumerate(self):
            if k == name:
                del self[i]
                return value
        return default

    def set_by_key(self, key: object, value: object, /) -> None:
        if value is not None:
            self.append((key, value))

    def copy(self) -> Self:
        return type(self)(self)

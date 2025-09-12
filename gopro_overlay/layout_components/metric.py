from typing import Callable, TypeVar, Optional

from pint import Quantity

from ..entry import Entry
from .text import text

T = TypeVar("T")


def metric_value(
        entry: Callable[[], Optional[Entry]],
        accessor: Callable[[Entry], Optional[Quantity]],
        converter: Callable[[Quantity], Optional[Quantity]],
        formatter: Callable[[Quantity], T],
        default: T = "-"
) -> Callable[[], T]:
    def value() -> T:
        e = accessor(entry())
        if e is not None:
            v = converter(e)
            if v is not None:
                return formatter(v)
        return default

    return value


def metric(entry, accessor, formatter, converter=lambda x: x, cache=True, **kwargs):
    return text(cache, value=metric_value(entry, accessor, converter, formatter), **kwargs)

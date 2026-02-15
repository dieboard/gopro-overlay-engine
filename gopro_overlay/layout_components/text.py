from ..widgets.text import CachingText, Text
from ..widgets.widgets import Widget


def text(cache=True, **kwargs) -> Widget:
    if cache:
        return CachingText(**kwargs)
    else:
        return Text(**kwargs)

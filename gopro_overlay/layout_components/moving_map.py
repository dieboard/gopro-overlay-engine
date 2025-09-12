from ..widgets.map import MovingMap
from ..widgets.widgets import Widget


def moving_map(at, entry, **kwargs) -> Widget:
    return MovingMap(
        at=at,
        location=lambda: entry().point,
        azimuth=lambda: entry().azi,
        **kwargs
    )

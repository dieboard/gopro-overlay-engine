from ..widgets.map import JourneyMap
from ..widgets.widgets import Widget


def journey_map(at, entry, **kwargs) -> Widget:
    return JourneyMap(
        at=at,
        location=lambda: entry().point,
        **kwargs
    )

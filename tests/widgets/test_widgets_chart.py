import itertools
from pathlib import Path

import pytest

from gopro_overlay.dimensions import Dimension
from gopro_overlay.ffmpeg import FFMPEG
from gopro_overlay.ffmpeg_gopro import FFMPEGGoPro
from gopro_overlay.framemeta import View, Window
from gopro_overlay.gpmd_filters import WorstOfGPSLockFilter, GPSLockTracker, GPSDOPFilter, GPSMaxSpeedFilter
from gopro_overlay.loading import GoproLoader
from gopro_overlay.point import Coordinate
from gopro_overlay.timeunits import timeunits
from gopro_overlay.units import units
from gopro_overlay.widgets.chart import SimpleChart
from gopro_overlay.widgets.widgets import Translate, Composite
from tests.approval import approve_image
from tests.widgets import test_widgets_setup
from tests.widgets.test_widgets import time_rendering

font = test_widgets_setup.font
title_font = test_widgets_setup.title_font
ts = test_widgets_setup.ts


@pytest.mark.gfx
@approve_image
def test_render_simple_chart():
    # Avg: 0.00018, Rate: 5,491.91
    view = View(data=list(itertools.chain(
        itertools.repeat(0, 128),
        itertools.repeat(1, 128)
    )), version=1)
    return time_rendering("Simple Chart", [
        Translate(
            at=Coordinate(50, 50),
            widget=SimpleChart(value=lambda: view, filled=True, font=font)
        )
    ])


@pytest.mark.gfx
@approve_image
def test_render_chart():
    # Avg: 0.00019, Rate: 5,325.79
    window = Window(
        ts,
        duration=timeunits(minutes=2),
        samples=256,
        key=lambda e: e.alt.magnitude,
    )

    view = window.view(ts.min)

    return time_rendering(
        name="Simple Chart with view",
        dimensions=Dimension(x=800, y=400),
        widgets=[
            Translate(
                at=Coordinate(0, 0),
                widget=Composite(
                    Translate(
                        at=Coordinate(0, 0),
                        widget=SimpleChart(
                            lambda: view,
                            filled=True,
                            font=font
                        )
                    ),
                    Translate(
                        at=Coordinate(0, 100),
                        widget=SimpleChart(
                            lambda: view,
                            filled=False,
                            font=font.font_variant(size=24)
                        )
                    ),
                    Translate(
                        at=Coordinate(0, 200),
                        widget=SimpleChart(
                            lambda: view,
                            filled=True,
                            font=font,
                            fill=(0, 255, 0, 128)
                        )
                    )
                )
            ),
            Translate(
                at=Coordinate(350, 0),
                widget=Composite(
                    Translate(
                        at=Coordinate(0, 0),
                        widget=SimpleChart(
                            lambda: view,
                            filled=True,
                            font=font.font_variant(size=32),
                            line=(255, 255, 0, 200)
                        )
                    ),
                    Translate(
                        at=Coordinate(0, 100),
                        widget=SimpleChart(
                            lambda: view,
                            filled=True,
                            font=font,
                            bg=(0, 0, 0),
                        )
                    ),
                    Translate(
                        at=Coordinate(0, 200),
                        widget=SimpleChart(
                            lambda: view,
                            filled=True,
                            font=font,
                            height=100,
                            fill=(0, 255, 0),
                            text=(0, 255, 255)
                        )
                    )
                )
            ),
        ])


@pytest.mark.gfx
@approve_image
def test_render_chart_with_no_data():
    window = Window(
        ts,
        duration=timeunits(minutes=2),
        samples=256,
        key=lambda e: e.bob.magnitude if e.bob else 0
    )

    view = window.view(ts.min)

    return time_rendering(name="Simple Chart with no valid data", widgets=[
        Translate(
            at=Coordinate(50, 50),
            widget=SimpleChart(lambda: view, filled=True, font=font.font_variant(size=64), height=200)
        )
    ])


# start = 0.04 / 24.52
@pytest.mark.gfx
@approve_image
def test_render_moving_chart():
    window = Window(
        ts,
        duration=timeunits(seconds=30),
        samples=512,
        key=lambda e: e.alt.magnitude,
    )

    stepper = iter(ts.stepper(timeunits(seconds=1)).steps())

    def get_view():
        return window.view(next(stepper))

    return time_rendering(name="Moving Chart", repeat=50, widgets=[
        Translate(
            at=Coordinate(50, 50),
            widget=SimpleChart(get_view, filled=True, font=font)
        )
    ])


def load_test_file(inputpath):
    if not inputpath.exists():
        pytest.xfail("contrib file not exist")

    loader = GoproLoader(
        ffmpeg_gopro=FFMPEGGoPro(FFMPEG()),
        units=units,
        gps_lock_filter=WorstOfGPSLockFilter(GPSLockTracker(), GPSDOPFilter(10), GPSMaxSpeedFilter(20))
    )

    gopro = loader.load(inputpath)

    return gopro.framemeta


@pytest.mark.gfx
def test_example_chart():
    test_file = Path("render/contrib/poor-gps/GX010303.MP4")

    ts = load_test_file(test_file)

    window = Window(
        ts,
        duration=timeunits(minutes=5),
        samples=256,
        key=lambda e: e.alt.magnitude,
    )

    time_rendering(name="Moving Chart", repeat=1, widgets=[
        Translate(
            at=Coordinate(50, 50),
            widget=SimpleChart(lambda: window.view(at=timeunits(seconds=(4 * 60) + 27)), filled=True, font=font)
        )
    ])

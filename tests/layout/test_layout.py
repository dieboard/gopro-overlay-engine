import random
from datetime import timedelta
from pathlib import Path

from gopro_overlay import fake, arguments
from gopro_overlay.dimensions import Dimension
from gopro_overlay.geo import MapRenderer, MapStyler
from gopro_overlay.layout import Overlay, speed_awareness_layout
from gopro_overlay.layout_xml import layout_from_xml, load_xml_layout, Converters
from gopro_overlay.privacy import NoPrivacyZone
from gopro_overlay.timing import PoorTimer
from gopro_overlay.widgets.widgets import SimpleFrameSupplier
from gopro_overlay.framemeta_csv import merge_csv_with_gopro
from tests.approval import approve_image
from tests.font import load_test_font
from tests.testenvironment import is_make

from datetime import datetime, timezone
from gopro_overlay.timeseries import Timeseries
from gopro_overlay.entry import Entry

# Need reproducible results for approval tests
rng = random.Random()
rng.seed(12345)

framemeta = fake.fake_framemeta(length=timedelta(minutes=10), step=timedelta(seconds=1), rng=rng)

renderer = MapRenderer(cache_dir=arguments.default_config_location, styler=MapStyler())

font = load_test_font()


@approve_image
def test_render_default_layout():
    # Avg: 0.01550, Rate: 64.53

    xmldoc = load_xml_layout(Path("default-1920x1080"))

    with renderer.open() as map_renderer:
        return time_layout("default", layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()))


@approve_image
def test_render_default_layout_different_units():
    xmldoc = load_xml_layout(Path("default-1920x1080"))

    with renderer.open() as map_renderer:
        return time_layout(
            "default",
            layout_from_xml(
                xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone(),
                converters=Converters(speed_unit="kph", temperature_unit="kelvin")
            )
        )


@approve_image
def test_render_default_layout_27k():
    xmldoc = load_xml_layout(Path("default-2704x1520"))

    with renderer.open() as map_renderer:
        return time_layout(
            "default",
            layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()),
            dimensions=Dimension(2704, 1520)
        )


@approve_image
def test_render_default_layout_4k():
    xmldoc = load_xml_layout(Path("default-3840x2160"))

    with renderer.open() as map_renderer:
        return time_layout(
            "default-4k",
            layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()),
            dimensions=Dimension(3840, 2160)
        )


@approve_image
def test_render_speed_layout():
    with renderer.open() as map_renderer:
        return time_layout("speed", speed_awareness_layout(map_renderer, font=font))


@approve_image
def test_render_example_layout():
    # Avg: 0.04147, Rate: 24.12
    xmldoc = load_xml_layout(Path("example"))

    with renderer.open() as map_renderer:
        return time_layout("xml", layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()))


@approve_image
def test_render_example_2_layout():
    xmldoc = load_xml_layout(Path("example-2"))

    with renderer.open() as map_renderer:
        return time_layout("xml", layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()))


@approve_image
def test_render_power_1920_1080():
    xmldoc = load_xml_layout(Path("power-1920x1080"))

    with renderer.open() as map_renderer:
        return time_layout("xml", layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()))


@approve_image
def test_render_xml_component():
    # Avg: 0.00169, Rate: 590.66
    xmldoc = """<layout>
        <composite name="bob" x="200" y="200">
            <component type="text" x="0" y="0" size="32">Text</component> 
            <component type="text" x="50" y="50" size="64">Text</component> 
            <component type="text" x="150" y="150" size="128" >Text</component> 
        </composite>
    </layout>
    """
    return do_layout(xmldoc)


@approve_image
def test_render_cairo_arc_annotated():
    xml = """
    <layout>
     <component type="cairo_gauge_arc_annotated" metric="speed" start="0" arc-value-lower="15" arc-value-upper="30" />
    </layout>
    """

    return do_layout(xml)


def do_layout(xmldoc):
    with renderer.open() as map_renderer:
        return time_layout("xml", layout_from_xml(xmldoc, map_renderer, framemeta, font, privacy=NoPrivacyZone()))


@approve_image
def test_render_xml_component_with_exclusions():
    # Avg: 0.00180, Rate: 556.84
    xmldoc = """<layout>
        <composite name="bob" x="200" y="200">
            <component type="text" x="0" y="0" size="32" cache="False">Bob</component> 
            <component type="text" x="50" y="50" size="64">Bob</component> 
            <component type="text" x="150" y="150" size="128" >Bob</component> 
        </composite>
        <composite name="alice" x="400" y="200">
            <component type="text" x="0" y="0" size="32">Alice</component> 
            <component type="text" x="50" y="50" size="64">Alice</component> 
            <component type="text" x="150" y="150" size="128" >Alice</component> 
        </composite>
    </layout>
    """

    with renderer.open() as map_renderer:
        return time_layout("xml",
                           layout_from_xml(
                               xmldoc,
                               map_renderer,
                               framemeta,
                               font,
                               privacy=NoPrivacyZone(),
                               include=lambda name: name == "alice"
                           ))


def time_layout(name, layout, repeat=20, dimensions=Dimension(1920, 1080)):
    supplier = SimpleFrameSupplier(dimensions)
    overlay = Overlay(framemeta=framemeta, create_widgets=layout)

    timer = PoorTimer(name)

    for i in range(0, repeat):
        draw = timer.time(lambda: overlay.draw(framemeta.mid, supplier.drawing_frame()))

    print(timer)

    if not is_make():
        draw.show()

    return draw


@approve_image
def test_render_location_component():
    csv_timeseries = ts(
        (0, {"street": "Street", "city": "City", "state": "State"})
    )
    merge_csv_with_gopro(csv_timeseries, framemeta)

    xmldoc = """<layout>
        <component type="text" x="0" y="0" size="16" align="left">Street: </component>
        <component type="metric" x="60" y="0" metric="street" size="16" align="left" cache="False"/>
        <component type="text" x="0" y="24" size="16" align="left">City: </component>
        <component type="metric" x="60" y="24" metric="city" size="16" align="left" cache="False"/>
        <component type="text" x="0" y="48" size="16" align="left">State: </component>
        <component type="metric" x="60" y="48" metric="state" size="16" align="left" cache="False"/>
    </layout>
    """
    return do_layout(xmldoc)

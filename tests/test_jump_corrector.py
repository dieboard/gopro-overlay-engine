
import pytest
from gopro_overlay.framemeta import FrameMeta
from gopro_overlay.point import Point
from gopro_overlay.entry import Entry
from gopro_overlay.timeunits import timeunits
from gopro_overlay.jump_corrector import analyze_and_correct_jump

def test_analyze_and_correct_jump_detects_and_fixes_jump():
    fm = FrameMeta()

    # Create a sequence of points with a jump
    # Points 0-9 are at "Home" (0, 0)
    # Point 10 jumps to "Start of Ride" (0.1, 0.1) - roughly 15km away, definitely a jump
    # Points 11+ continue at "Start of Ride"

    # 0.001 degrees is roughly 111 meters
    # 500 meters is roughly 0.0045 degrees

    start_lat = 51.0
    start_lon = 0.0

    # 0.1 degrees is approx 11km
    jump_lat = 51.1
    jump_lon = 0.1

    # Create 10 points at incorrect location
    for i in range(10):
        t = timeunits(seconds=i)
        fm.add(t, Entry(dt=None, point=Point(start_lat, start_lon)))

    # Create 10 points at correct location
    for i in range(10, 20):
        t = timeunits(seconds=i)
        fm.add(t, Entry(dt=None, point=Point(jump_lat, jump_lon)))

    fm._update() # Ensure internal lists are updated

    assert fm.get(timeunits(seconds=0)).point.lat == start_lat

    analyze_and_correct_jump(fm)

    # Check if points before jump are corrected
    for i in range(10):
        pt = fm.get(timeunits(seconds=i)).point
        assert pt.lat == jump_lat
        assert pt.lon == jump_lon

    # Check points after jump are untouched
    for i in range(10, 20):
        pt = fm.get(timeunits(seconds=i)).point
        assert pt.lat == jump_lat
        assert pt.lon == jump_lon

def test_analyze_and_correct_jump_no_jump():
    fm = FrameMeta()

    start_lat = 51.0
    start_lon = 0.0

    # Create 20 points moving slowly
    for i in range(20):
        t = timeunits(seconds=i)
        # Move very slightly
        lat = start_lat + (i * 0.00001)
        fm.add(t, Entry(dt=None, point=Point(lat, start_lon)))

    fm._update()

    original_pt_0 = fm.get(timeunits(seconds=0)).point

    analyze_and_correct_jump(fm)

    new_pt_0 = fm.get(timeunits(seconds=0)).point

    assert original_pt_0.lat == new_pt_0.lat

def test_analyze_and_correct_jump_stops_after_max_duration():
    fm = FrameMeta()

    start_lat = 51.0
    start_lon = 0.0
    jump_lat = 51.1
    jump_lon = 0.1

    # Jump happens at 3 minutes (180 seconds), which is after the 2 minute check

    # 0 to 179 seconds at start location
    for i in range(180):
        t = timeunits(seconds=i)
        fm.add(t, Entry(dt=None, point=Point(start_lat, start_lon)))

    # 180+ at new location
    for i in range(180, 200):
        t = timeunits(seconds=i)
        fm.add(t, Entry(dt=None, point=Point(jump_lat, jump_lon)))

    fm._update()

    analyze_and_correct_jump(fm)

    # Should NOT have corrected anything because jump is after 2 mins
    pt_0 = fm.get(timeunits(seconds=0)).point
    assert pt_0.lat == start_lat

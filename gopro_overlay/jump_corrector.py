import datetime
from typing import Optional

from gopro_overlay.framemeta import FrameMeta
from gopro_overlay.log import log
from gopro_overlay.point import Point
from gopro_overlay.timeunits import timeunits, Timeunit

def distance(p1: Point, p2: Point) -> float:
    """Calculates distance between two points in meters using Haversine formula"""
    import math
    R = 6371e3 # Earth radius in meters
    phi1 = p1.lat * math.pi / 180
    phi2 = p2.lat * math.pi / 180
    dphi = (p2.lat - p1.lat) * math.pi / 180
    dlambda = (p2.lon - p1.lon) * math.pi / 180

    a = math.sin(dphi/2) * math.sin(dphi/2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(dlambda/2) * math.sin(dlambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def analyze_and_correct_jump(framemeta: FrameMeta):
    log("Analyzing GPS data for initial jumps...")

    # Only check first 2 minutes or less if data is shorter
    max_duration = timeunits(minutes=2)
    start_time = framemeta.min
    end_scan_time = start_time + max_duration

    # Threshold for jump - e.g. 500 meters
    JUMP_THRESHOLD_METERS = 500.0

    framelist = framemeta.framelist
    frames = framemeta.frames

    last_point: Optional[Point] = None
    jump_found_at: Optional[Timeunit] = None
    correct_point: Optional[Point] = None

    # Iterate through frames
    for i, t in enumerate(framelist):
        if t > end_scan_time:
            break

        entry = frames[t]
        # entry.point should be the location
        # need to check if entry has 'point' attribute
        if not hasattr(entry, 'point') or entry.point is None:
            continue

        current_point = entry.point

        if last_point is not None:
            dist = distance(last_point, current_point)
            if dist > JUMP_THRESHOLD_METERS:
                log(f"Found GPS jump of {dist:.2f}m at {t} (index {i})")
                jump_found_at = t
                correct_point = current_point
                break

        last_point = current_point

    if jump_found_at is not None and correct_point is not None:
        log(f"Correcting GPS data before {jump_found_at} to {correct_point}")

        # Update all points before the jump
        count = 0
        for t in framelist:
            if t >= jump_found_at:
                break

            entry = frames[t]
            if hasattr(entry, 'point'):
                entry.update(point=correct_point)
                count += 1

        log(f"Corrected {count} frames.")
    else:
        log("No initial GPS jump found.")

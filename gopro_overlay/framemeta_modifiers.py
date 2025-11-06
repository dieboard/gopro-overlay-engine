from gopro_overlay.framemeta import FrameMeta
from gopro_overlay.gpmf.gpmf import GPSFix
from gopro_overlay.point import Point
from gopro_overlay.timeseries import Entry
from gopro_overlay.timeunits import timeunits
from gopro_overlay.units import units


def filter_gps_jumps(framemeta: FrameMeta, max_speed):
    # a simplistic filter that looks for the first time the GPS seems to be settled.
    # It calculates the speed between points, if the speed is too high, it assumes the point is still settling
    # once it finds a point that isn't moving impossibly fast, it sets all previous points to that location
    # and sets GPS lock to 2D

    first_good_sample = -1

    # an iterator that skips the first one
    items = framemeta.items()
    next(items)

    for index, entry in enumerate(items):
        # index is +1 as we skipped the first
        index = index + 1

        previous = framemeta[index-1]
        metres = entry.point.distance(previous.point)
        seconds = (entry.timestamp - previous.timestamp).us / 1000000.0
        speed = metres / seconds
        if speed > max_speed:
            first_good_sample = index
            break

    if first_good_sample > 0:
        first_good_entry = framemeta[first_good_sample]
        first_good_point = first_good_entry.point

        for i in range(0, first_good_sample):
            framemeta[i].point = first_good_point
            framemeta[i].gpsfix = GPSFix.LOCK_2D
            framemeta[i].dop = 10.0

        framemeta[first_good_sample].gpsfix = GPSFix.LOCK_2D
        framemeta[first_good_sample].dop = 10.0

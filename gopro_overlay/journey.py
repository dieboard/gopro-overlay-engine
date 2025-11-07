import datetime
import math
from itertools import tee
from typing import List

from haversine import haversine

from .gpmf import GPS_FIXED_VALUES
from .point import Point, BoundingBox
from .timeseries import MovingAverage


def rich(journey):
    j = Journey(
        locations=journey.locations,
        lat=journey.lat,
        lon=journey.lon,
        badlat=journey.badlat,
        badlon=journey.badlon
    )
    j.calculate()
    return j

class MinMax:

    def __init__(self, name):
        self._items = []
        self._name = name

    @property
    def name(self):
        return self._name

    def update(self, new):
        if new is not None:
            self._items.append(new)

    def __len__(self):
        return len(self._items)

    @property
    def min(self):
        return min(self._items)

    @property
    def max(self):
        return max(self._items)

    def __str__(self):
        return f"{self.name}: min:{self.min} max:{self.max}"


class Extents:

    def __init__(self):
        self.lat = MinMax("lat")
        self.lon = MinMax("lon")
        self.velocity = MinMax("velocity")
        self.altitude = MinMax("altitude")
        self.cadence = MinMax("cadence")
        self.hr = MinMax("hr")

    def accept(self, item):
        self.velocity.update(item.speed)
        self.altitude.update(item.alt)
        self.cadence.update(item.cad)
        self.hr.update(item.hr)


MIN_BOX_SIZE = 0.0001


class NullJourney:

    def distance(self):
        return 0

    def duration(self):
        return datetime.timedelta(seconds=0)

    def speed_at(self, dt):
        return 0

    def distance_from(self, dt):
        return 0

    def distance_to(self, dt):
        return 0

    def max_speed(self):
        return 0

    def average_speed(self):
        return 0


class Journey:

    def __init__(self, locations=None, lat=None, lon=None, badlat=None, badlon=None):
        self.locations: List[Point] = locations or []
        self.lat = lat or MinMax("lat")
        self.lon = lon or MinMax("lon")
        self.badlat = badlat or MinMax("badlat")
        self.badlon = badlon or MinMax("badlon")

        self._distance = 0
        self._cumulative_distance = MovingAverage()
        self._speed = MovingAverage()

    def accept(self, item):
        if item.gpsfix in GPS_FIXED_VALUES:
            item.point.dt = item.dt
            self.locations.append(item.point)
            self.lat.update(item.point.lat)
            self.lon.update(item.point.lon)
        else:
            self.badlat.update(item.point.lat)
            self.badlon.update(item.point.lon)

    def calculate(self):
        if self.locations:
            self._cumulative_distance.add(self.locations[0].dt, 0)

            a, b = tee(self.locations)
            next(b, None)
            for start, end in zip(a, b):
                metres = haversine((start.lat, start.lon), (end.lat, end.lon)) * 1000
                self._distance += metres

                duration = (end.dt - start.dt).total_seconds()
                if duration > 0:
                    self._speed.add(start.dt, metres / duration)
                self._cumulative_distance.add(end.dt, self._distance)
            self._speed.add(self.locations[-1].dt, 0)

    @property
    def bounding_box(self) -> BoundingBox:
        lat = self.lat if self.lat else self.badlat
        lon = self.lon if self.lon else self.badlon

        if math.dist([lat.min, lon.min], [lat.max, lon.max]) < MIN_BOX_SIZE:
            return BoundingBox(Point(lat.min, lon.min), Point(lat.min + MIN_BOX_SIZE, lon.min + MIN_BOX_SIZE))

        return BoundingBox(Point(lat.min, lon.min), Point(lat.max, lon.max))

    def distance(self):
        return self._distance

    def duration(self):
        return self.locations[-1].dt - self.locations[0].dt

    def speed_at(self, dt):
        return self._speed.get(dt)

    def distance_from(self, dt):
        return self._distance - self.distance_to(dt)

    def distance_to(self, dt):
        return self._cumulative_distance.get(dt)

    def max_speed(self):
        return self._speed.max()

    def average_speed(self):
        return self.distance() / self.duration().total_seconds()

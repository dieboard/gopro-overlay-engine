
from gopro_overlay.journey import Journey, NullJourney
from gopro_overlay.point import Point

class JourneyMeta:
    def __init__(self, journey: Journey):
        self.journey = journey

    def distance(self):
        return self.journey.distance()

    def speed(self, point: Point):
        return self.journey.speed_at(point.dt)

    def average_speed(self):
        return self.journey.distance() / self.journey.duration()

    def top_speed(self):
        return self.journey.max_speed()

    def remaining_distance(self, point: Point):
        return self.journey.distance_from(point.dt)

class NullJourneyMeta(JourneyMeta):
    def __init__(self):
        super().__init__(NullJourney())

    def distance(self):
        return 0

    def speed(self, point: Point):
        return 0

    def average_speed(self):
        return 0

    def top_speed(self):
        return 0

    def remaining_distance(self, point: Point):
        return 0

import csv
from datetime import datetime

from gopro_overlay.entry import Entry
from gopro_overlay.point import Point
from gopro_overlay.timeseries import Timeseries


def load_csv_timeseries(filepath, units) -> Timeseries:
    timeseries = Timeseries()

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = datetime.fromisoformat(row["time"])
            timeseries.add(
                dt,
                Entry(
                    dt=dt,
                    point=Point(lat=float(row["lat"]), lon=float(row["lon"])),
                    alt=units.Quantity(float(row["alt"]), units.m),
                    street=row["street"],
                    state=row["state"],
                )
            )

    return timeseries


def merge_csv_with_gopro(csv_timeseries: Timeseries, gopro_framemeta):
    def processor(gopro_entry):
        try:
            csv_entry = csv_timeseries.get(gopro_entry.dt)
            return {"street": csv_entry.street, "state": csv_entry.state}
        except ValueError:
            pass

    gopro_framemeta.process(processor)

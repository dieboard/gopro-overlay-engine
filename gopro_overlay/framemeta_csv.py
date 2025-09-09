import csv
from datetime import datetime

from gopro_overlay.entry import Entry
from gopro_overlay.log import log
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
                    street=row["street"],
                    state=row["state"],
                )
            )

    return timeseries


def merge_csv_with_gopro(csv_timeseries: Timeseries, gopro_framemeta):
    log("Attempting to merge CSV data...")
    if len(csv_timeseries) > 0:
        log(f"CSV time range: {csv_timeseries.min} -> {csv_timeseries.max}")
    else:
        log("CSV timeseries is empty.")

    if len(gopro_framemeta) > 0:
        log(f"GPX/video time range: {gopro_framemeta.date_at(gopro_framemeta.min)} -> {gopro_framemeta.date_at(gopro_framemeta.max)}")
    else:
        log("GoPro framemeta is empty.")

    def processor(gopro_entry):
        try:
            csv_entry = csv_timeseries.get(gopro_entry.dt)
            gopro_entry.update(street=csv_entry.street, state=csv_entry.state)
        except ValueError:
            pass

    gopro_framemeta.process(processor)

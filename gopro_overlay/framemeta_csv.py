import csv
from datetime import datetime
from gopro_overlay.entry import Entry
from gopro_overlay.log import log
from gopro_overlay.timeseries import Timeseries
from pathlib import Path

# This corrected version handles both file paths and in-memory streams
def load_csv_timeseries(source, units) -> Timeseries:
    timeseries = Timeseries()

    # This inner function does the actual reading from a stream
    def process(stream):
        reader = csv.DictReader(stream)
        for row in reader:
            if not row or not row.get("time"):
                continue
            dt = datetime.fromisoformat(row["time"])
            entry = Entry(
                dt=dt,
                street=row.get("street"),
                city=row.get("city"),
                state=row.get("state"),
            )
            timeseries.add(entry)

    # We check if the input 'source' is a path on the disk
    if isinstance(source, (str, Path)):
        # If it is, we open the file and process it
        with open(source, "r") as f:
            process(f)
    else:
        # If not, we assume it's already a stream (like StringIO) and process it directly
        process(source)

    return timeseries

# The merge function doesn't need to be changed
def merge_csv_with_gopro(csv_timeseries: Timeseries, gopro_framemeta):
    log("Attempting to merge CSV data...")
    if len(csv_timeseries) > 0:
        log(f"CSV time range: {csv_timeseries.min} -> {csv_timeseries.max}")
    else:
        log("CSV timeseries is empty.")

    if len(gopro_framemeta) > 0:
        log(f"GPX/video time range: {gopro_framemeta.get(gopro_framemeta.min).dt} -> {gopro_framemeta.get(gopro_framemeta.max).dt}")
    else:
        log("GoPro framemeta is empty.")

    def processor(gopro_entry):
        try:
            csv_entry = csv_timeseries.get(gopro_entry.dt)
            gopro_entry.update(street=csv_entry.street, city=csv_entry.city, state=csv_entry.state)
        except ValueError:
            pass

    gopro_framemeta.process(processor)
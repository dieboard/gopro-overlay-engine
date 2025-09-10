from gopro_overlay.framemeta_csv import load_csv_timeseries, merge_csv_with_gopro
from gopro_overlay.units import units
from gopro_overlay.timeseries import Timeseries
from gopro_overlay.entry import Entry
from tests.test_timeseries import datetime_of
from io import StringIO

def test_load_csv():
    csv_data = "time,street,city,state\\n2023-01-01T12:00:00+00:00,Dummy Street,Dummy City,Dummy State\\n"
    timeseries = load_csv_timeseries(StringIO(csv_data), units)

    assert len(timeseries) == 1
    entry = timeseries.get(datetime_of(1672574400))
    assert entry.street == "Dummy Street"
    assert entry.city == "Dummy City"
    assert entry.state == "Dummy State"

def test_merge_csv():
    csv_data = "time,street,city,state\\n2023-01-01T12:00:00+00:00,Dummy Street,Dummy City,Dummy State\\n"
    csv_timeseries = load_csv_timeseries(StringIO(csv_data), units)

    framemeta = Timeseries()
    entry_to_update = Entry(dt=datetime_of(1672574400))
    framemeta.add(entry_to_update)

    merge_csv_with_gopro(csv_timeseries, framemeta)

    updated_entry = framemeta.get(datetime_of(1672574400))
    assert updated_entry.street == "Dummy Street"
    assert updated_entry.city == "Dummy City"
    assert updated_entry.state == "Dummy State"

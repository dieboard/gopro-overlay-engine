from datetime import datetime, timedelta, timezone

from gopro_overlay.framemeta import FrameMeta
from gopro_overlay.framemeta_modifiers import filter_gps_jumps
from gopro_overlay.gpmf.gpmf import GPSFix
from gopro_overlay.point import Point
from gopro_overlay.timeseries import Entry
from gopro_overlay.units import units


def test_filter_gps_jumps():
    framemeta = FrameMeta(packets_per_second=1)
    start_dt = datetime.now(timezone.utc)
    framemeta.add(units.Quantity(0, units.s), Entry(
        dt=start_dt + timedelta(seconds=0),
        timestamp=units.Quantity(0, units.s),
        point=Point(52.3906479, 5.2975658),
        gpsfix=GPSFix.NO,
        dop=100.0,
    ))
    framemeta.add(units.Quantity(1, units.s), Entry(
        dt=start_dt + timedelta(seconds=1),
        timestamp=units.Quantity(1, units.s),
        point=Point(52.3906480, 5.2975659),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))
    framemeta.add(units.Quantity(2, units.s), Entry(
        dt=start_dt + timedelta(seconds=2),
        timestamp=units.Quantity(2, units.s),
        point=Point(52.1008679, 5.0604441),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))
    framemeta.add(units.Quantity(3, units.s), Entry(
        dt=start_dt + timedelta(seconds=3),
        timestamp=units.Quantity(3, units.s),
        point=Point(52.1008637, 5.0604401),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))

    filter_gps_jumps(framemeta, max_speed=50)

    assert framemeta[0].point == Point(52.1008679, 5.0604441)
    assert framemeta[1].point == Point(52.1008679, 5.0604441)
    assert framemeta[2].point == Point(52.1008679, 5.0604441)
    assert framemeta[3].point == Point(52.1008637, 5.0604401)

    assert framemeta[0].gpsfix == GPSFix.LOCK_2D
    assert framemeta[1].gpsfix == GPSFix.LOCK_2D
    assert framemeta[2].gpsfix == GPSFix.LOCK_3D

    # and this one isn't modified
    assert framemeta[3].gpsfix == GPSFix.LOCK_3D

    assert framemeta[0].dop == 10.0
    assert framemeta[1].dop == 10.0
    assert framemeta[2].dop == 1.0

    # and this one isn't modified
    assert framemeta[3].dop == 1.0

from datetime import datetime, timedelta, timezone

from gopro_overlay.framemeta import FrameMeta
from gopro_overlay.framemeta_modifiers import filter_gps_jumps
from gopro_overlay.gpmf.gpmf import GPSFix
from gopro_overlay.point import Point
from gopro_overlay.timeseries import Entry
from gopro_overlay.timeunits import timeunits
from gopro_overlay.units import units


def test_filter_gps_jumps():
    framemeta = FrameMeta(packets_per_second=1)
    start_dt = datetime.now(timezone.utc)
    framemeta.add(timeunits(seconds=0), Entry(
        dt=start_dt + timedelta(seconds=0),
        timestamp=timeunits(seconds=0),
        point=Point(52.3906479, 5.2975658),
        gpsfix=GPSFix.NO,
        dop=100.0,
    ))
    framemeta.add(timeunits(seconds=1), Entry(
        dt=start_dt + timedelta(seconds=1),
        timestamp=timeunits(seconds=1),
        point=Point(52.3906480, 5.2975659),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))
    framemeta.add(timeunits(seconds=2), Entry(
        dt=start_dt + timedelta(seconds=2),
        timestamp=timeunits(seconds=2),
        point=Point(52.1008679, 5.0604441),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))
    framemeta.add(timeunits(seconds=3), Entry(
        dt=start_dt + timedelta(seconds=3),
        timestamp=timeunits(seconds=3),
        point=Point(52.1008637, 5.0604401),
        gpsfix=GPSFix.LOCK_3D,
        dop=1.0,
    ))

    filter_gps_jumps(framemeta, max_speed=20)

    assert framemeta[0].point == Point(52.1008679, 5.0604441)
    assert framemeta[1].point == Point(52.1008679, 5.0604441)
    assert framemeta[2].point == Point(52.1008679, 5.0604441)
    assert framemeta[3].point == Point(52.1008637, 5.0604401)

    assert framemeta[0].gpsfix == GPSFix.LOCK_2D
    assert framemeta[1].gpsfix == GPSFix.LOCK_2D
    assert framemeta[2].gpsfix == GPSFix.LOCK_2D

    # and this one isn't modified
    assert framemeta[3].gpsfix == GPSFix.LOCK_3D

    assert framemeta[0].dop == 10.0
    assert framemeta[1].dop == 10.0
    assert framemeta[2].dop == 10.0

    # and this one isn't modified
    assert framemeta[3].dop == 1.0

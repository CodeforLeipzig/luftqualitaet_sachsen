from measuring_stations.models import MeasuringPoint


def test_active_values():
    mp = MeasuringPoint(so2=True, o3=True)
    assert mp.active_values == ('so2', 'o3')

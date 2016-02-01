from measuring_stations.models import MeasuringPoint
import pytest


def test_active_values():
    mp = MeasuringPoint(so2=True, o3=True)
    assert mp.get_active_values() == ('so2', 'o3')


@pytest.fixture
def csv():
    return "Datum Zeit; Leipzig-Mitte SO2\n" \
           "; <B5>g/m<B3>\n" \
           "01-07-14 11:00; 4,0\n" \
           "01-07-14 10:00; 4,1"


@pytest.fixture
def params():
    return []


@pytest.fixture
def stationName():
    return "Leipzig-Mitte"


def test_import_values(csv, stationName, params):
    pytest.mark.django_db(transaction=False)

    mp = MeasuringPoint()
    mp.put_csv(csv, stationName, params)

    # assert

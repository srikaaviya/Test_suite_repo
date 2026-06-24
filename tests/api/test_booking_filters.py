import pytest
from src.models import create_test_booking


@pytest.mark.api
def test_filter_by_firstname(api_client):
    data = create_test_booking(firstname="Uniquefilterfirst")
    api_client.create_booking(data)

    response = api_client.get_booking_ids({"firstname": "Uniquefilterfirst"})
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.api
def test_filter_by_lastname(api_client):
    data = create_test_booking(lastname="Uniquefilterlast")
    api_client.create_booking(data)

    response = api_client.get_booking_ids({"lastname": "Uniquefilterlast"})
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.api
def test_filter_by_checkin_date(api_client):
    data = create_test_booking()
    api_client.create_booking(data)

    response = api_client.get_booking_ids({"checkin": "2026-01-01"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.api
def test_filter_by_checkout_date(api_client):
    data = create_test_booking()
    api_client.create_booking(data)

    response = api_client.get_booking_ids({"checkout": "2026-01-10"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.api
def test_filter_by_name_combination(api_client):
    data = create_test_booking(firstname="ComboFirst", lastname="ComboLast")
    api_client.create_booking(data)

    response = api_client.get_booking_ids({
        "firstname": "ComboFirst",
        "lastname": "ComboLast",
    })
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.api
def test_filter_by_nonexistent_name_returns_empty(api_client):
    response = api_client.get_booking_ids({"firstname": "Zzzznotarealname99999"})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.api
def test_filter_by_invalid_date_format(api_client):
    response = api_client.get_booking_ids({"checkin": "not-a-date"})
    assert response.status_code in [200, 400, 500]


@pytest.mark.api
def test_filter_with_no_params_returns_all(api_client):
    response = api_client.get_booking_ids()
    assert response.status_code == 200
    assert len(response.json()) > 0
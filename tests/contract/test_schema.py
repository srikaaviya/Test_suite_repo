import pytest
from src.models import create_test_booking


BOOKING_FIELDS = {"firstname", "lastname", "totalprice", "depositpaid", "bookingdates"}
DATE_FIELDS = {"checkin", "checkout"}


@pytest.mark.contract
def test_create_booking_response_schema(api_client):
    data = create_test_booking()
    response = api_client.create_booking(data)
    body = response.json()

    assert "bookingid" in body
    assert "booking" in body
    assert isinstance(body["bookingid"], int)

    booking = body["booking"]
    assert BOOKING_FIELDS.issubset(booking.keys())


@pytest.mark.contract
def test_get_booking_response_schema(api_client, created_booking):
    booking_id, _ = created_booking
    response = api_client.get_booking(booking_id)
    booking = response.json()

    assert BOOKING_FIELDS.issubset(booking.keys())
    assert isinstance(booking["firstname"], str)
    assert isinstance(booking["lastname"], str)
    assert isinstance(booking["totalprice"], int)
    assert isinstance(booking["depositpaid"], bool)


@pytest.mark.contract
def test_booking_dates_schema(api_client, created_booking):
    booking_id, _ = created_booking
    response = api_client.get_booking(booking_id)
    dates = response.json()["bookingdates"]

    assert DATE_FIELDS.issubset(dates.keys())
    assert isinstance(dates["checkin"], str)
    assert isinstance(dates["checkout"], str)


@pytest.mark.contract
def test_get_booking_ids_response_schema(api_client):
    response = api_client.get_booking_ids()
    body = response.json()

    assert isinstance(body, list)
    assert len(body) > 0
    assert "bookingid" in body[0]


@pytest.mark.contract
def test_auth_response_schema():
    import requests
    from src.config import BASE_URL, REQUEST_TIMEOUT

    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=REQUEST_TIMEOUT,
    )
    body = response.json()

    assert "token" in body
    assert isinstance(body["token"], str)


@pytest.mark.contract
def test_create_booking_preserves_data(api_client):
    data = create_test_booking(
        firstname="Contract",
        lastname="Test",
        totalprice=999,
        depositpaid=False,
    )
    response = api_client.create_booking(data)
    booking = response.json()["booking"]

    assert booking["firstname"] == "Contract"
    assert booking["lastname"] == "Test"
    assert booking["totalprice"] == 999
    assert booking["depositpaid"] is False
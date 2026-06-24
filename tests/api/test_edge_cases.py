import pytest
from src.models import create_test_booking


@pytest.mark.api
def test_create_booking_empty_body(api_client):
    response = api_client.create_booking({})
    assert response.status_code in [400, 500]


@pytest.mark.api
def test_create_booking_missing_required_fields(api_client):
    response = api_client.create_booking({"firstname": "OnlyFirst"})
    assert response.status_code in [400, 500]


@pytest.mark.api
def test_create_booking_invalid_date_format(api_client):
    data = create_test_booking()
    data["bookingdates"]["checkin"] = "not-a-date"
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400, 500]


@pytest.mark.api
def test_create_booking_negative_price(api_client):
    data = create_test_booking(totalprice=-100)
    response = api_client.create_booking(data)
    assert response.status_code == 200


@pytest.mark.api
def test_create_booking_extremely_long_name(api_client):
    data = create_test_booking(firstname="A" * 10000)
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400, 413, 500]


@pytest.mark.api
def test_update_without_auth_returns_403(client_no_auth, created_booking):
    booking_id, _ = created_booking
    data = create_test_booking(firstname="Hacker")
    response = client_no_auth.update_booking(booking_id, data)
    assert response.status_code == 403


@pytest.mark.api
def test_delete_without_auth_returns_403(client_no_auth, created_booking):
    booking_id, _ = created_booking
    response = client_no_auth.delete_booking(booking_id)
    assert response.status_code == 403


@pytest.mark.api
def test_get_nonexistent_booking_returns_404(api_client):
    response = api_client.get_booking(9999999)
    assert response.status_code == 404


@pytest.mark.api
def test_create_booking_with_extra_fields(api_client):
    data = create_test_booking()
    data["roomtype"] = "suite"
    data["vipstatus"] = True
    response = api_client.create_booking(data)
    assert response.status_code == 200


@pytest.mark.api
def test_create_booking_with_special_characters(api_client):
    data = create_test_booking(firstname="O'Brien", lastname="Müller-Schmidt")
    response = api_client.create_booking(data)
    assert response.status_code == 200


@pytest.mark.api
def test_create_booking_with_past_dates(api_client):
    data = create_test_booking()
    data["bookingdates"]["checkin"] = "2020-01-01"
    data["bookingdates"]["checkout"] = "2020-01-05"
    response = api_client.create_booking(data)
    assert response.status_code == 200


@pytest.mark.api
def test_checkout_before_checkin(api_client):
    data = create_test_booking()
    data["bookingdates"]["checkin"] = "2026-06-10"
    data["bookingdates"]["checkout"] = "2026-06-05"
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400]
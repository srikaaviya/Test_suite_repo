import pytest
from src.models import create_test_booking


@pytest.mark.api
@pytest.mark.smoke
def test_create_booking_returns_200(api_client, sample_booking):
    response = api_client.create_booking(sample_booking)
    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.smoke
def test_create_booking_response_contains_id(api_client, sample_booking):
    response = api_client.create_booking(sample_booking)
    body = response.json()
    assert "bookingid" in body
    assert isinstance(body["bookingid"], int)


@pytest.mark.api
@pytest.mark.smoke
def test_get_booking_by_id(api_client, created_booking):
    booking_id, booking_data = created_booking
    response = api_client.get_booking(booking_id)
    assert response.status_code == 200
    assert response.json()["firstname"] == booking_data["firstname"]
    assert response.json()["lastname"] == booking_data["lastname"]


@pytest.mark.api
def test_get_all_booking_ids(api_client):
    response = api_client.get_booking_ids()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


@pytest.mark.api
@pytest.mark.smoke
def test_update_booking_with_token(api_client, created_booking):
    booking_id, booking_data = created_booking
    updated_data = create_test_booking(firstname="Updated", lastname="Name")
    response = api_client.update_booking(booking_id, updated_data)
    assert response.status_code == 200
    assert response.json()["firstname"] == "Updated"


@pytest.mark.api
def test_partial_update_booking(api_client, created_booking):
    booking_id, booking_data = created_booking
    response = api_client.partial_update_booking(booking_id, {"firstname": "Patched"})
    assert response.status_code == 200
    assert response.json()["firstname"] == "Patched"


@pytest.mark.api
@pytest.mark.smoke
def test_delete_booking_with_token(api_client):
    data = create_test_booking()
    create_response = api_client.create_booking(data)
    booking_id = create_response.json()["bookingid"]

    delete_response = api_client.delete_booking(booking_id)
    assert delete_response.status_code == 201


@pytest.mark.api
def test_deleted_booking_returns_404(api_client):
    data = create_test_booking()
    create_response = api_client.create_booking(data)
    booking_id = create_response.json()["bookingid"]

    api_client.delete_booking(booking_id)
    get_response = api_client.get_booking(booking_id)
    assert get_response.status_code == 404
import pytest
from src.models import create_test_booking


@pytest.fixture()
def sample_booking():
    return create_test_booking()


@pytest.fixture()
def created_booking(api_client):
    data = create_test_booking()
    response = api_client.create_booking(data)
    body = response.json()
    booking_id = body["bookingid"]

    yield booking_id, body["booking"]

    api_client.delete_booking(booking_id)
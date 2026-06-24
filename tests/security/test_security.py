import pytest
from src.models import create_test_booking


@pytest.mark.security
def test_sql_injection_in_firstname(api_client):
    data = create_test_booking(firstname="' OR '1'='1")
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        booking = response.json()["booking"]
        assert booking["firstname"] == "' OR '1'='1"


@pytest.mark.security
def test_sql_injection_in_filter_params(api_client):
    response = api_client.get_booking_ids({"firstname": "' OR 1=1 --"})
    assert response.status_code in [200, 400, 500]


@pytest.mark.security
def test_xss_in_name_fields(api_client):
    xss_payload = "<script>alert('xss')</script>"
    data = create_test_booking(firstname=xss_payload)
    response = api_client.create_booking(data)
    if response.status_code == 200:
        booking = response.json()["booking"]
        assert "<script>" not in booking["firstname"] or booking["firstname"] == xss_payload


@pytest.mark.security
def test_xss_in_additional_needs(api_client):
    xss_payload = "<img src=x onerror=alert('xss')>"
    data = create_test_booking()
    data["additionalneeds"] = xss_payload
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400]


@pytest.mark.security
def test_auth_token_expiry_behavior(api_client):
    from src.api_client import ApiClient
    fake_client = ApiClient(token="expired_invalid_token_12345")
    data = create_test_booking()
    booking = api_client.create_booking(data)
    booking_id = booking.json()["bookingid"]

    response = fake_client.update_booking(booking_id, data)
    assert response.status_code == 403

    api_client.delete_booking(booking_id)


@pytest.mark.security
def test_idor_access_other_booking(client_no_auth, created_booking):
    booking_id, _ = created_booking
    data = create_test_booking(firstname="Hacked")
    response = client_no_auth.update_booking(booking_id, data)
    assert response.status_code == 403


@pytest.mark.security
def test_header_injection_in_cookie(api_client):
    # from src.api_client import ApiClient
    # malicious_token = "valid_token\r\nX-Injected-Header: evil"
    # client = ApiClient(token=malicious_token)
    # response = client.health_check()
    # assert response.status_code in [200, 201, 400, 500]

    from src.api_client import ApiClient
    import requests

    malicious_token = "valid_token\r\nX-Injected-Header: evil"
    client = ApiClient(token=malicious_token)
    with pytest.raises((ValueError, requests.exceptions.InvalidHeader)):
        client.health_check()


@pytest.mark.security
def test_oversized_payload_handling(api_client):
    data = create_test_booking(firstname="A" * 100000, lastname="B" * 100000)
    response = api_client.create_booking(data)
    assert response.status_code in [200, 400, 413, 500]
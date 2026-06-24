import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_health_check_returns_201(api_client):
    response = api_client.health_check()
    assert response.status_code == 201


@pytest.mark.api
def test_health_check_response_time(api_client):
    response = api_client.health_check()
    assert response.elapsed.total_seconds() < 2


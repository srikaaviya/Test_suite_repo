import pytest
import requests
from src.config import BASE_URL, REQUEST_TIMEOUT


@pytest.mark.api
@pytest.mark.smoke
def test_auth_with_valid_credentials():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=REQUEST_TIMEOUT,
    )
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.api
def test_auth_token_is_string():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=REQUEST_TIMEOUT,
    )
    assert isinstance(response.json()["token"], str)
    assert len(response.json()["token"]) > 0


@pytest.mark.api
def test_auth_with_invalid_credentials():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "wrong", "password": "wrong"},
        timeout=REQUEST_TIMEOUT,
    )
    assert response.status_code == 200
    assert response.json().get("reason") == "Bad credentials"


@pytest.mark.api
def test_auth_with_empty_body():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={},
        timeout=REQUEST_TIMEOUT,
    )
    assert response.json().get("reason") == "Bad credentials"


@pytest.mark.api
def test_auth_with_missing_password():
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": "admin"},
        timeout=REQUEST_TIMEOUT,
    )
    assert response.json().get("reason") == "Bad credentials"
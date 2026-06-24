import requests
from src.config import BASE_URL, AUTH_USERNAME, AUTH_PASSWORD, REQUEST_TIMEOUT


def get_auth_token() -> str:
    response = requests.post(
        f"{BASE_URL}/auth",
        json={"username": AUTH_USERNAME, "password": AUTH_PASSWORD},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["token"]
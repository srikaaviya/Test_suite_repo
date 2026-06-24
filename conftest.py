import pytest
from src.auth import get_auth_token
from src.api_client import ApiClient


@pytest.fixture(scope="session")
def auth_token():
    return get_auth_token()


@pytest.fixture(scope="session")
def api_client(auth_token):
    return ApiClient(token=auth_token)


@pytest.fixture()
def client_no_auth():
    return ApiClient()
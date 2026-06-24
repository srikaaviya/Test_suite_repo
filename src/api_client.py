import requests
from src.config import BASE_URL, REQUEST_TIMEOUT


class ApiClient:
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        if token:
            self.session.cookies.set("token", token)
        self.base_url = BASE_URL
        self.timeout = REQUEST_TIMEOUT

    def health_check(self) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/ping",
            timeout=self.timeout,
        )

    def create_booking(self, data: dict) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/booking",
            json=data,
            timeout=self.timeout,
        )

    def get_booking(self, booking_id: int) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/booking/{booking_id}",
            timeout=self.timeout,
        )

    def get_booking_ids(self, params: dict = None) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/booking",
            params=params,
            timeout=self.timeout,
        )

    def update_booking(self, booking_id: int, data: dict) -> requests.Response:
        return self.session.put(
            f"{self.base_url}/booking/{booking_id}",
            json=data,
            timeout=self.timeout,
        )

    def partial_update_booking(self, booking_id: int, data: dict) -> requests.Response:
        return self.session.patch(
            f"{self.base_url}/booking/{booking_id}",
            json=data,
            timeout=self.timeout,
        )

    def delete_booking(self, booking_id: int) -> requests.Response:
        return self.session.delete(
            f"{self.base_url}/booking/{booking_id}",
            timeout=self.timeout,
        )
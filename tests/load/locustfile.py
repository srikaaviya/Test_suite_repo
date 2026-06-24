from locust import HttpUser, task, between
from src.models import create_test_booking


class BookingUser(HttpUser):
    host = "https://restful-booker.herokuapp.com"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/auth",
            json={"username": "admin", "password": "password123"},
        )
        self.token = response.json().get("token", "")

    @task(5)
    def get_booking_ids(self):
        self.client.get("/booking")

    @task(3)
    def get_single_booking(self):
        ids_response = self.client.get("/booking")
        ids = ids_response.json()
        if ids:
            booking_id = ids[0]["bookingid"]
            self.client.get(f"/booking/{booking_id}")

    @task(2)
    def create_booking(self):
        data = create_test_booking()
        self.client.post("/booking", json=data)

    @task(1)
    def update_booking(self):
        data = create_test_booking()
        create_response = self.client.post("/booking", json=data)
        if create_response.status_code == 200:
            booking_id = create_response.json()["bookingid"]
            updated = create_test_booking(firstname="Updated")
            self.client.put(
                f"/booking/{booking_id}",
                json=updated,
                cookies={"token": self.token},
            )
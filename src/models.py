from pydantic import BaseModel
from datetime import date


class BookingDates(BaseModel):
    checkin: str = "2026-01-01"
    checkout: str = "2026-01-10"


class Booking(BaseModel):
    firstname: str = "James"
    lastname: str = "Brown"
    totalprice: int = 150
    depositpaid: bool = True
    bookingdates: BookingDates = BookingDates()
    additionalneeds: str = "Breakfast"


def create_test_booking(**overrides) -> dict:
    booking = Booking(**overrides)
    return booking.model_dump()
    #converts to a plain dict that requests can send as JSON
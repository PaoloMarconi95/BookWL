from enum import Enum

class BookingResult(Enum):
    SUCCESS = 1
    WAITLIST = 2
    ALREADY_BOOKED = 3
    FAIL = 4
    NOT_FOUND = 5
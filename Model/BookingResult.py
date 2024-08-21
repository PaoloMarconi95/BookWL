from enum import Enum


class BookingResult(Enum):
    SUCCESS = 1
    WAITLIST = 2
    FAIL = 3
    NOT_FOUND = 4

import datetime
import time

from playwright.sync_api import Locator

from Config import LOGGER
from Config.FutureBookingConfiguration import ClassToBeBooked


def book_class(cl: ClassToBeBooked, rows: dict[datetime, list[Locator]]) -> None:
    row_class_to_book = None
    for row in rows[cl.date.date()]:
        if cl.name in row.inner_text() and cl.program in row.inner_text():
            row_class_to_book = row

    if row_class_to_book is not None:
        book_button = row_class_to_book.locator('a[id*="wtAddReservationLink2"]')
        if book_button is not None:
            book_button.click()
            time.sleep(0.5)
        else:
            LOGGER.warn(f"Book button for class {cl.name} was not found")
    else:
        LOGGER.warn(f"No corresponding class row found for class {cl.name}")

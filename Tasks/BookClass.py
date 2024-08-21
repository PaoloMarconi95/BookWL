import datetime
import time

from playwright.sync_api import Locator

from Config import LOGGER
from Config.FutureBookingConfiguration import ClassToBeBooked


def book_class(class_to_book: ClassToBeBooked, rows: dict[datetime, list[Locator]]) -> None:
    row_class_to_book = None
    for row in rows[class_to_book.date]:
        inner_text = row.inner_text()
        if class_to_book.name in inner_text and class_to_book.program in inner_text:
            row_class_to_book = row

    if row_class_to_book is not None:
        book_button = row_class_to_book.locator('a[id*="wtAddReservationLink2"]')
        if book_button.count() > 0:
            book_button.click()
            time.sleep(0.5)
        else:
            LOGGER.warn(f"Book button for class {class_to_book.name} was not found")
    else:
        LOGGER.warn(f"No corresponding class row found for class {class_to_book.name}")

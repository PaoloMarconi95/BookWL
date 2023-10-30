# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Standard
import time
from datetime import datetime

# Custom
from Config import CONFIG, LOGGER
from Exceptions import NoReservationFoundException
from Enum.BookingResult import BookingResult


def is_class_name_matching(book, text_found):
    class_name = book.class_name.lower()
    class_time = book.class_time
    text_found = text_found.lower()
    if class_name in text_found and str(class_time) in text_found:
        return True
    return False


"""
:param classes is an array of selenium WebElement
:param class_name is the string representing the class name
:return the clickable element that sends the desired reservation when clicked
"""
def find_booking_row_by_book(classes, book):
    booking_row = list(filter(lambda daily_class: is_class_name_matching(book, daily_class.text), classes))
    if len(booking_row) == 1:
        booking_row = booking_row[0]
        try:
            # Find the Reservation Icon
            booking_el = WebDriverWait(booking_row, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[class='icon icon-calendar']")))
        except (NoSuchElementException, TimeoutException):
            booking_row.find_element(By.CLASS_NAME, 'icon-forbidden')
            LOGGER.info('No icon calendar found for ' + str(book.class_name) + ' at ' + str(book.date))
            booking_el = None
        return booking_el, booking_row
    else:
        raise NoReservationFoundException


# def find_ticket_icon(book, wd):
#     LOGGER.info('find_ticket_icon started')
#     try:
#         classes = get_all_classes_for_date(book.date, wd)
#         _, booking_row = find_booking_row_by_book(classes, book)
#         LOGGER.info('booking row correctly retrieved')
#         booking_row.find_element(By.CLASS_NAME, 'icon-ticket')
#         return True
#     except NoSuchElementException as e:
#         LOGGER.warn('Did not find icon svg' + str(e))
#         return False

def is_icon_present_in_row(booking_row, css_class):
    # css class should be either icon-ticket or icon-forbidden
    try:
        booking_row.find_element(By.CLASS_NAME, css_class)
        return True
    except NoSuchElementException:
        return False



# Expects a string date with format dd-MM-yyyy
def set_date(date, wd):
    LOGGER.info('Setting date to ' + date)
    element = wd.find_element(By.ID, "AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom")
    element.clear()
    element.send_keys(date)


def get_all_classes_for_date(date, wd):
    set_date(date, wd)
    # Waiting for site backend to render new date's data
    time.sleep(3)

    table_entries = wd.find_elements(By.XPATH, '//table/tbody/tr')
    # First elements is always the calendar filter
    table_entries.pop(0)

    daily_classes = []
    for index, el in enumerate(table_entries):
        # Day title does not have style attribute, while class rows have it
        if index == 0 and el.get_attribute("style") == '':
            # If there's a title in first row, skip it
            continue
        elif index > 0 and el.get_attribute("style") == '':
            # Next title reached (day after the selected date)
            return daily_classes
        else:
            # Class row encountered, add it to daily classes
            daily_classes.append(el)


def get_booked_class_and_program_for_date(date, wd):
    set_date(date, wd)
    # Waiting for site backend to render new date's data
    time.sleep(3)

    table_entries = wd.find_elements(By.XPATH, '//table/tbody/tr')
    # First elements is always the calendar filter, so discard it
    table_entries.pop(0)

    string_target = str(int(datetime.strftime(datetime.today(), "%H")) + 1)
    # string_target = "19"

    for index, el in enumerate(table_entries):
        # Day title does not have style attribute, while class rows have it
        if index == 0 and el.get_attribute("style") == '':
            # If there's a title in first row, skip it
            continue
        elif index > 0 and el.get_attribute("style") == '':
            # Next title reached (day after the selected date)
            return None
        else:
            try:
                el.find_element(By.CLASS_NAME, 'icon-ticket')
                title_el = el.find_element(By.XPATH, './/td/div/span')
                if string_target in title_el.text:
                    return el
            except NoSuchElementException:
                # Class may be not booked or concerns another hour
                continue


def analyze_booking_result(booking_row):
    if booking_row is None:
        return BookingResult.FAIL

    icon_present = is_icon_present_in_row(booking_row, 'icon-ticket')
    forbidden_present = is_icon_present_in_row(booking_row, 'icon-forbidden')

    if icon_present and forbidden_present:
        return BookingResult.SUCCESS
    if not icon_present and forbidden_present:
        return BookingResult.WAITLIST

    return BookingResult.FAIL

def book_class(book, wd):
    result = None
    wd.get(CONFIG.calendar_url)
    try:
        classes = get_all_classes_for_date(book.date, wd)
        LOGGER.info("found " + str(len(classes)) + " classes for " + str(book.date))
        booking_el, booking_row = find_booking_row_by_book(classes, book)
        if booking_el is not None:
            booking_el.click()
            # Wait for the reservation to be sent
            wd.refresh()
            classes = get_all_classes_for_date(book.date, wd)
            _, booking_row = find_booking_row_by_book(classes, book)
            result = analyze_booking_result(booking_row)
        else:
            return BookingResult.ALREADY_BOOKED
    except NoSuchElementException:
        LOGGER.info('Make Reservation title not found, could be already booked or not opened yet')
    except NoReservationFoundException:
        return BookingResult.NOT_FOUND

    return result
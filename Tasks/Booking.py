# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Standard
import time
from datetime import datetime

# Custom
import Log
import Configuration
from Exceptions import NoReservationFoundException

log = Log.logger
config = Configuration.get_instance()
driver = config.driver


def is_class_name_matching(book, text_found):
    class_name = book.class_name.lower()
    class_time = book.class_time.lower()
    text_found = text_found.lower()
    if class_name and class_time in text_found:
        return True
    return False


def find_booking_row_by_book(classes, book):
    """
    :param classes is an array of selenium WebElement
    :param book is the string representing the class name
    :return the clickable element that sends the desired reservation when clicked
    """
    booking_row = list(filter(lambda daily_class: is_class_name_matching(book, daily_class.text), classes))
    if len(booking_row) == 1:
        booking_row = booking_row[0]
        try:
            # Find the Reservation Icon
            booking_el = booking_row.find_element(By.XPATH, ".//a[@title='Make Reservation']")
        except NoSuchElementException:
            booking_row.find_element(By.CLASS_NAME, 'icon-ticket')
            log.info('Reservation already made for ' + str(book.class_name) + ' at ' + str(book.date))
            booking_el = None
        return booking_el, booking_row
    else:
        raise NoReservationFoundException


def find_ticket_icon(book):
    log.info('find_ticket_icon started')
    try:
        classes = get_all_classes_for_date(book.date)
        _, booking_row = find_booking_row_by_book(classes, book)
        log.info('booking row correctly retrieved')
        booking_row.find_element(By.CLASS_NAME, 'icon-ticket')
        return True
    except NoSuchElementException as e:
        log.warn('Did not find icon svg' + str(e))
        return False


# Expects a string date with format dd-MM-yyyy
def set_date(date):
    log.info('Setting date to ' + date)
    element = driver.find_element(By.ID,
                                  "AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom")
    element.clear()
    element.send_keys(date)


def get_all_classes_for_date(date):
    set_date(date)
    # Waiting for site backend to render new date's data
    time.sleep(4)

    table_entries = driver.find_elements(By.XPATH, '//table/tbody/tr')
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


def get_booked_classes_for_date(date):
    set_date(date)
    # Waiting for site backend to render new date's data
    time.sleep(4)

    table_entries = driver.find_elements(By.XPATH, '//table/tbody/tr')
    # First elements is always the calendar filter
    table_entries.pop(0)

    string_target = str(int(datetime.strftime(datetime.today(), "%H")) + 1)
    # string_target = "18"

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
                    # Class row encountered, add it to daily classes
                    return el
            except NoSuchElementException:
                # Class may be not booked or concerns another hour
                continue


def book_class(book):
    success = False
    driver.get(config.calendar_url)
    try:
        classes = get_all_classes_for_date(book.date)
        log.info("found " + str(len(classes)) + " classes for " + str(book.date))
        booking_el, booking_row = find_booking_row_by_book(classes, book)
        if booking_el is not None:
            booking_el.click()
            # Wait for the reservation to be sent
            driver.refresh()
            success = find_ticket_icon(book)
    except NoSuchElementException:
        log.info('Make Reservation title not found, could be already booked or not opened yet')

    return success

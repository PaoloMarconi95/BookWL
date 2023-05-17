# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Standard
from datetime import datetime
import time

# Custom
import Log
import Tasks.Configuration as Configuration

log = Log.logger
driver = Configuration.driver
config = Configuration.conf


"""
:param classes is an array of selenium WebElement
:param class_name is the string representing the class name
:return the clickable element that sends the desired reservation when clicked
"""
def find_booking_element_by_class_name(classes, class_name):
    class_row = list(filter(lambda daily_class: class_name in daily_class.text, classes))[0]
    if class_row is not None:
        booking_el = class_row.find_element(By.XPATH, ".//a[@title='Make Reservation']")
        return booking_el
    else:
        return None


def find_ticket_icon(booked_row):
    if booked_row is None:
        return False
    try:
        booked_row.find_element(By.CSS_SELECTOR, '.icon.icon-ticket')
        return True
    except NoSuchElementException:
        log.info('Did not find icon svg')
        return False


# Expects a string date with format dd-MM-yyyy
def set_date(date):
    log.info('Setting date to ' + date)
    element = driver.find_element(By.ID, "AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom")
    element.clear()
    element.send_keys(date)


def get_all_classes_for_date(date):
    set_date(datetime.strftime(date, '%d-%m-%y'))
    # Waiting for site backend to render new date's data
    time.sleep(4)

    table_entries = driver.find_elements(By.XPATH, '//table/tbody/tr')
    # First elements is always the calendar filter
    table_entries.pop()

    daily_classes = []
    for index, el in enumerate(table_entries):
        # Day title does not have style attribute, while class rows have it
        if index == 0 and el.get_attribute("style") == '':
            # If there's a title in first row, skip it
            continue
        elif index > 0 and el.get_attribute("style") == '':
            # Next title reached
            return daily_classes
        else:
            # Class row encountered, add it to daily classes
            daily_classes.append(el)

def book_class(book):
    driver.get(config.calendar_url)
    try:
        classes = get_all_classes_for_date(book.date)
        log.info("found " + str(len(classes)) + " classes for " + str(book.date))
        booking_el = find_booking_element_by_class_name(classes, book.class_name)
        if booking_el is not None:
            booking_el.click()
        else:
            log.warn("Did not find any " + str(book.class_name) + " for " + str(book.date))
        success = find_ticket_icon(booking_el)
    except NoSuchElementException:
        success = False
        log.info('Make Reservation title not found, could be already booked or not opened yet')

    return success
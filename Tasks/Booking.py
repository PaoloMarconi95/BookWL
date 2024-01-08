# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

# Standard
import time

# Custom
from Config import CONFIG, LOGGER
from DB.Entities.CrossFitClass import CrossFitClass
from Exceptions import NoReservationFoundException
from Enum.BookingResult import BookingResult
from DB.Entities.FutureBooking import FutureBooking
from Utils.dateUtils import get_formatted_date
    

def find_clickable_booking_element(booking_row):
    try:
        # Find the Reservation Icon
        booking_el = WebDriverWait(booking_row, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[class*='icon icon-calendar']")))
    except (NoSuchElementException, TimeoutException):
        booking_el = None
    return booking_el
    

def find_booked_rows(classes: list, class_name=None) -> list:
    booked_classes = []
    # If crossfit_class is valorized, then filter out 
    classes = find_row_for_class_name(classes, class_name)    
    for cl in classes:
        if is_icon_present_in_row(cl, 'icon-forbidden'):
            booked_classes.append(cl)
    return booked_classes


def find_row_for_class_name(classes: list, class_name: str) -> list:
    if class_name is not None:
        classes = list(filter(lambda daily_class: class_name in daily_class.text, classes))
    if len(classes) > 1:
        raise Exception(f"Too many booked classes found for {class_name}")
    if len(classes) == 0:
        raise NoReservationFoundException
    
    return classes


def is_icon_present_in_row(booking_row, css_class: str) -> bool:
    # css class should be either icon-ticket or icon-forbidden
    try:
        booking_row.find_element(By.CLASS_NAME, css_class)
        return True
    except NoSuchElementException:
        return False



# Expects a string date with format dd-MM-yyyy
def set_date(date, wd):
    element = wd.find_element(By.ID, "AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom")
    if element.get_attribute('value') != date:
        LOGGER.info('Setting date to ' + date)
        element.clear()
        element.send_keys(date)
        time.sleep(3)


def get_all_classes_for_date(wd, date)-> list:
    set_date(date, wd)

    try:
        title = WebDriverWait(wd, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='h3']")))
        formattedDate = get_formatted_date(date, '%d-%m-%Y')
        if formattedDate not in title.text:
            LOGGER.error(f"No date {date} found within title {title.text}!")
            return []            
    except NoSuchElementException:
        LOGGER.error(f"No title found for date {date}!")
        return []

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


def get_booked_row_for_datetime(wd, date, hour):
    set_date(date, wd)

    table_entries = wd.find_elements(By.XPATH, '//table/tbody/tr')
    # First elements is always the calendar filter, so discard it
    table_entries.pop(0)

    #string_target = "18"
    string_target = f"{hour}"

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


def analyze_booking_result(booking_row) -> BookingResult:
    if booking_row is None:
        LOGGER.warn("Booking row is none, failed to book current class")
        return BookingResult.FAIL

    ticket_present = is_icon_present_in_row(booking_row, 'icon-ticket')
    forbidden_present = is_icon_present_in_row(booking_row, 'icon-forbidden')

    if ticket_present and forbidden_present:
        return BookingResult.SUCCESS
    if not ticket_present and forbidden_present:
        return BookingResult.WAITLIST

    LOGGER.warn(f"Failed to book current class, ticket: {ticket_present}, forbidden_present: {forbidden_present}")
    return BookingResult.FAIL


def book_class(book: FutureBooking, wd) -> BookingResult:
    wd.get(CONFIG.calendar_url)
    try:
        classes = get_all_classes_for_date(wd, book.class_date)
        if len(classes) == 0:
            return BookingResult.NOT_FOUND
        LOGGER.info("found " + str(len(classes)) + " classes for " + str(book.class_date))
        booked_row = find_row_for_class_name(classes, book.class_name)
        booking_button = find_clickable_booking_element(booked_row[0])
        if booking_button is not None:
            booking_button.click()
            # Wait for the reservation to be sent
            wd.refresh()
            time.sleep(1)
            classes = get_all_classes_for_date(wd, book.class_date)
            booked_row = find_row_for_class_name(classes, book.class_name)
            result = analyze_booking_result(booked_row[0])
        else:
            return BookingResult.ALREADY_BOOKED
    except NoSuchElementException:
        LOGGER.info('Make Reservation title not found, could be already booked or not opened yet')
    except NoReservationFoundException:
        return BookingResult.NOT_FOUND

    return result


def is_still_booked(crossfit_class: CrossFitClass, wd) -> bool:
    classes = get_all_classes_for_date(wd, crossfit_class.date)
    booked_rows = find_booked_rows(classes, crossfit_class.name)
    if len(booked_rows) == 1:
        LOGGER.info(f'crossfit class {crossfit_class} still booked!')
        return True
    else:
        LOGGER.info(f'crossfit class {crossfit_class} not booked anymore! Avoiding the sign-in')
        return False
    
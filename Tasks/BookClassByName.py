# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Standard
from datetime import datetime

# Custom
import Log
import Tasks.Configuration as Configuration

log = Log.logger
driver = Configuration.driver
config = Configuration.conf


def find_booking_element_by_class_name(class_name):
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + class_name + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    booking_el = wl_class_row.find_element(By.XPATH, ".//a[@title='Make Reservation']")
    return booking_el


def find_ticket_icon(class_name):
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + class_name + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    try:
        wl_class_row.find_element(By.CSS_SELECTOR, '.icon.icon-ticket')
        return True
    except NoSuchElementException:
        log.info('Didn\'t find icon svg')
        return False



# Expects a string date with format dd-MM-yyyy
def set_date(date):
    log.info('Setting date to ' + date)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, 'AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom'))
    )
    element.clear()
    element.send_keys(date)

def book_class(book):
    driver.get(config.calendar_url)
    set_date(datetime.strftime(book.date, '%d-%m-%y'))
    try:
        wl_booking_el = find_booking_element_by_class_name(book.class_name)
        wl_booking_el.click()
        success = True
    except NoSuchElementException:
        success = False
        log.info('Make Reservation title not found, could be already booked or not opened yet')

    return success
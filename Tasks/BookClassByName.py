# Selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Custom
from Log import Log
Log = Log.get_instance()


def find_booking_element_by_class_name(driver, class_name):
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + class_name + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    booking_el = wl_class_row.find_element(By.XPATH, ".//a[@title='Make Reservation']")
    return booking_el


def find_ticket_icon(driver, class_name):
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + class_name + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    try:
        wl_class_row.find_element(By.CSS_SELECTOR, '.icon.icon-ticket')
        return True
    except NoSuchElementException:
        Log.info('Didn\'t find icon svg')
        return False


def book_class_by_name(driver, class_name):
    try:
        wl_booking_el = find_booking_element_by_class_name(driver, class_name)
        wl_booking_el.click()
        success = True
    except NoSuchElementException:
        success = False
        Log.info('Make Reservation title not found, could be already booked or not opened yet')

    return success

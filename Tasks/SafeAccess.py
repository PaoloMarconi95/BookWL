# Standard
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import traceback

# Custom
import Log
from SendEmail import send_email

log = Log.logger


def safe_access_by_id(driver, id_string, max_attempts=5):
    element = None
    attempts = 0
    while attempts == 0 or (not EC.staleness_of(element) and attempts <= max_attempts):
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, id_string))
            )
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            traceback.print_exc()
            log.warn(f"{id_string} retrieval failed, I'm going to refresh driver and wait for 2 seconds.")
            driver.refresh()
            time.sleep(2)
        finally:
            attempts += 1

    if attempts < max_attempts and element is not None:
        return element
    else:
        log.error(f'Safe access to element {id_string} failed')
        return None

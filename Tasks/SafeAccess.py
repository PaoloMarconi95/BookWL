# Standard
import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import traceback

# Custom
from Config import LOGGER
from Utils.debugCurrentStatus import save_html_to_file

def safe_access(driver, identifier, max_attempts=5, by=By.ID):
    element = None
    attempts = 0
    while attempts == 0 or (not EC.staleness_of(element) and attempts <= max_attempts):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, identifier))
            )
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            now = datetime.now()
            id = f"{now.day}-{now.month}_{now.hour}:{now.minute}_a{attempts}"
            save_html_to_file(driver, id)
            traceback.print_exc()
            LOGGER.warn(f"{identifier} retrieval failed, I'm going to refresh driver and wait for 2 seconds.")
            driver.refresh()
            time.sleep(5)
        finally:
            attempts += 1

    if attempts < max_attempts and element is not None:
        return element
    else:
        LOGGER.error(f'Safe access to element {identifier} failed')
        return None

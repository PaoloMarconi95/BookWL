# Standard
import time
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import traceback

# Custom
from Config import LOGGER, CONFIG

def safe_access_by_id(driver, identifyier, max_attempts=5, by=By.ID):
    element = None
    attempts = 0
    while attempts == 0 or (not EC.staleness_of(element) and attempts <= max_attempts):
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, identifyier))
            )
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            with open(os.path.join(CONFIG.html_file_path, f'debug_{attempts}.html'), 'w+') as f:
                f.write(driver.page_source)
            traceback.print_exc()
            LOGGER.warn(f"{identifyier} retrieval failed, I'm going to refresh driver and wait for 2 seconds.")
            driver.refresh()
            time.sleep(2)
        finally:
            attempts += 1

    if attempts < max_attempts and element is not None:
        return element
    else:
        LOGGER.error(f'Safe access to element {identifyier} failed')
        return None

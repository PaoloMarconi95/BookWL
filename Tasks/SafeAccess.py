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
            LOGGER.warn(f"{id_string} retrieval failed, I'm going to refresh driver and wait for 10 seconds.")

            html_file_name = f"{id_string}_{attempts}.html"
            html_file_path = os.path.join(CONFIG.html_file_path, html_file_name)
            with open(html_file_path, 'w+') as html_file:
                LOGGER.info(f'printing html to file {html_file_path}')
                html_file.write(driver.page_source)

            time.sleep(5)
            driver.refresh()
            time.sleep(5)
        finally:
            attempts += 1

    if attempts < max_attempts and element is not None:
        return element
    else:
        LOGGER.error(f'Safe access to element {id_string} failed')
        return None

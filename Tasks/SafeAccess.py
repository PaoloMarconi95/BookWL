# Standard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# Custom
import Log
log = Log.logger

def safe_access_by_id(element, driver, max_attempts=5):
    attempts = 0
    while not EC.staleness_of(element) and attempts < max_attempts:
        element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.ID, 'FormLogin'))
        )
        attempts += 1

    if attempts < max_attempts:
        return True
    else:
        return False

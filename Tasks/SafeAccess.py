# Standard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import traceback

# Custom
import Log
from SendEmail import send_email

log = Log.logger

def safe_access_by_id(driver, id_string, max_attempts=5):
    # First retrieval attempt
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, id_string))
    )

    attempts = 0
    while not EC.staleness_of(element) and attempts < max_attempts:
        try:
            log.warn('stale element found, trying to re-define it')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, id_string))
            )
        except (NoSuchElementException, StaleElementReferenceException) as e:
            traceback.print_exc()
            send_email("paolomarconi1995@gmail.com", "Eccezione Verificata! Controlla Il log", str(e))
        finally:
            attempts += 1

    if attempts < max_attempts:
        return element
    else:
        log.error(f'Safe access to element {id_string} failed')
        return None

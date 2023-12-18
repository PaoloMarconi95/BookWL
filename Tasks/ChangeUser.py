from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Custom
from Config import LOGGER

def log_out(user, wd):
    LOGGER.info(f"Logging out {user.name}")
    logout_el = WebDriverWait(wd, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[text()="Logout"]'))
    )
    logout_el.click()
    LOGGER.info(f"Log out for {user.name} completed")
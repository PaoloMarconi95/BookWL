from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Custom
import Log
import Configuration

log = Log.logger
config = Configuration.get_instance()


def log_out(user, wd):
    name = user.name
    log.info(f"Logging out {name if name is not None else ''}")
    logout_el = WebDriverWait(wd, 5).until(
        EC.presence_of_element_located((By.XPATH, '//a[text()="Logout"]'))
    )
    logout_el.click()
    #time.sleep(3)
    log.info(f"Log out for {name if name is not None else ''} completed")

# Standard
import time
from datetime import datetime

# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Custom
import Log
import Configuration

config = Configuration.get_instance()
driver = config.driver
log = Log.logger
attempts = 1

def login(user, max_attempts=4):
    global attempts
    logged_id = False

    while (attempts < max_attempts) and not logged_id:
        try:
            driver.get(config.calendar_url)
            time.sleep(4)
            login_el = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.ID, 'FormLogin'))
            )
            EC.staleness_of(login_el)
            log.info("Logging in at " + str(datetime.now().time()))
            username_el = login_el.find_element(By.ID, 'Input_UserName')
            username_el.send_keys(user.username)
            pwd_el = login_el.find_element(By.ID, 'Input_Password')
            pwd_el.send_keys(user.pwd)
            submit_el = login_el.find_element(By.TAG_NAME, 'button')
            submit_el.click()
            calendar_el = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'AthleteTheme_wt6_block_wtMain'))
            )
            if calendar_el is not None:
                log.info('Successfully logged in')
                logged_id = True
        except Exception as e:
            attempts += 1
            log.error(f'Error during login process, {str(max_attempts - attempts)} attempts remaining')
            raise e

    attempts = 0
    return logged_id


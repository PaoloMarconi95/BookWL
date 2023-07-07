# Standard
import time
from datetime import datetime

# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Custom
import Log
import Configuration
from Tasks.SafeAccess import safe_access_by_id

config = Configuration.get_instance()
driver = config.driver
log = Log.logger

def login(user):
    logged_id = False
    driver.get(config.calendar_url)
    time.sleep(2)
    login_el = safe_access_by_id(driver, 'FormLogin')
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
    return logged_id


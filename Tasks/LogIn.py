# Standard
import time
from datetime import datetime

# Selenium
from selenium.webdriver.common.by import By

# Custom
import Log
import Configuration
from Tasks.SafeAccess import safe_access_by_id

config = Configuration.get_instance()
#driver = config.driver
log = Log.logger

def login(user, wd):
    logged_id = False
    wd.get(config.calendar_url)
    log.info("Logging in at " + str(datetime.now().time()))
    #time.sleep(2)
    login_el = safe_access_by_id(wd, 'FormLogin')
    log.info("Log in element found")
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    log.info("username_el found")
    username_el.send_keys(user.username)
    log.info("username_el sent")
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    log.info("pwd_el found")
    pwd_el.send_keys(user.pwd)
    log.info("pwd_el sent")
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    log.info("submit_el found")
    submit_el.click()
    log.info("submit_el clicked, now waiting for calendar el...")


    calendar_el = None
    try:
        calendar_el = safe_access_by_id(wd, 'AthleteTheme_wt6_block_wtMain')
    except Exception as e:
        log.error(str(e))

    if calendar_el is not None:
        log.info('Successfully logged in')
        logged_id = True
    return logged_id


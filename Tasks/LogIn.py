# Standard
from datetime import datetime


# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Custom
import Log
import Tasks.Configuration as Configuration

config = Configuration.conf
driver = Configuration.driver
log = Log.logger

def login():
    driver.get(config.calendar_url)
    login_el = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'FormLogin'))
    )
    log.info("Logging in at " + str(datetime.now().time()))
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    username_el.send_keys(config.username)
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    pwd_el.send_keys(config.password)
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    submit_el.click()
    completed = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wt6_block_wtMain'))
    )
    if completed is not None:
        log.info('Successfully logged in')
    else:
        log.error('Did not recognize successful Log in, did not find AthleteTheme_wt6_block_wtMain')
        raise NoSuchElementException('LogIn process failed, did not recognize calendar url post login')

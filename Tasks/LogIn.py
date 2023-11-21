# Standard
from datetime import datetime

# Selenium
from selenium.webdriver.common.by import By

# Custom
from Config import CONFIG, LOGGER
from Tasks.SafeAccess import safe_access_by_id

def login(user, wd):
    logged_id = False
    wd.get(CONFIG.calendar_url)
    LOGGER.info("Logging in at " + str(datetime.now().time()))
    #time.sleep(2)
    login_el = safe_access_by_id(wd, 'FormLogin')
    LOGGER.info("Log in element found")
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    LOGGER.info("username_el found")
    username_el.send_keys(user.username)
    LOGGER.info("username_el sent")
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    LOGGER.info("pwd_el found")
    pwd_el.send_keys(user.pwd)
    LOGGER.info("pwd_el sent")
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    LOGGER.info("submit_el found")
    submit_el.click()
    LOGGER.info("submit_el clicked, now waiting for calendar el...")


    calendar_el = None
    try:
        calendar_el = safe_access_by_id(wd, CONFIG.calendar_el_id)
    except Exception as e:
        LOGGER.error(str(e))

    if calendar_el is not None:
        LOGGER.info(f'User {user.name} successfully logged in!')
        logged_id = True
    return logged_id


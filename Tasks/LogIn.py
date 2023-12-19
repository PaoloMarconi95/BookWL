# Selenium
from selenium.webdriver.common.by import By

# Custom
from Config import CONFIG, LOGGER
from Tasks.SafeAccess import safe_access_by_id
from DB.Entities.User import User

def login(user: User, wd) -> bool:
    logged_in = False
    attempts = 0
    while not logged_in and attempts < CONFIG.max_login_attempts:
        try:
            logged_in = perform_login(user, wd)
            logged_in = True
        except AttributeError as e:
            LOGGER.error(f'Login for user {user.name} failed! ({e}) Trying again...')
        finally:
            attempts += 1
    
    return logged_in



def perform_login(user: User, wd):
    wd.get(CONFIG.calendar_url)
    login_el = safe_access_by_id(wd, 'FormLogin')
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    username_el.send_keys(user.mail)
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    pwd_el.send_keys(user.password)
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    submit_el.click()
    LOGGER.info("submit_el clicked, now waiting for calendar el...")

    calendar_el = None
    try:
        calendar_el = safe_access_by_id(wd, CONFIG.calendar_el_id)
    except Exception as e:
        LOGGER.error(str(e))

    logged_id = False
    if calendar_el is not None:
        LOGGER.info(f'User {user.name} successfully logged in!')
        return True
    return False



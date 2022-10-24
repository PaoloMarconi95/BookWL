# Standard
import json

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

import Tasks.BusyWait
# Custom
from Exceptions import GlobalVariablesNotSetException
from Log import Log
from Tasks.ChromeDriverUpdater import update_chromedriver

MAX_ATTEMPTS = 30
PROCEDURE_START_AT = '16:56:00'
FIRE_START_AT = '16:59:12'
CLASS_TARGET = 'WEIGHTLIFTING 19.00'
MAX_START_ATTEMPTS = 3
Log = Log.get_instance()


def start():
    print('startato')


def initialize_process():
    start_attempts = 0
    are_variables_set = False
    while not are_variables_set and start_attempts != MAX_START_ATTEMPTS:
        try:
            # Main Exception may occur from a non-updated version of chromedriver
            set_global_variables()
            are_variables_set = True
        except GlobalVariablesNotSetException:
            are_variables_set = update_chromedriver()
            start_attempts += 1
            Log.info('set_global_variables, ' + str(MAX_START_ATTEMPTS - start_attempts) + ' attempts remaining')
            if are_variables_set:
                Log.info('chromedriver updated, trying to redefine global variables')
                set_global_variables()

    return are_variables_set


def set_global_variables():
    global driver

    f = open('config.json', 'r')
    config = json.load(f)
    url = config['CALENDAR_URL']
    f.close()

    options = Options()
    options.headless = False  # set it to True only in prod mode
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
    except (SessionNotCreatedException, WebDriverException, FileNotFoundError):
        Log.warn('Error occurred in driver initialization. Trying to retrieve an updated version of chromedriver...')
        raise GlobalVariablesNotSetException


if __name__ == '__main__':
    global driver

    # Try to initialize global variables
    is_initialized = initialize_process()

    # If ChromeDriverUpdater terminated correctly, proceed with booking algorithm
    if is_initialized:
        Log.info('Instance correctly initialized')
        Tasks.BusyWait.until(PROCEDURE_START_AT)
        start()
    else:
        Log.error('System failed to initialize session. check log for more info')

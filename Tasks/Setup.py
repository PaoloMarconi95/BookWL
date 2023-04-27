# Standard
import json
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# Custom
from Exceptions import GlobalVariablesNotSetException
from Tasks.ChromeDriverUpdater import update_chromedriver
from Log import Log
Log = Log.get_instance()

MAX_START_ATTEMPTS = 3
initialized_driver = None

def initialize_process():
    start_attempts = 1
    are_variables_set = False
    # Terminate the loop when variables are successfully set or max attempts are reached
    while (not are_variables_set) and (start_attempts <= MAX_START_ATTEMPTS):
        try:
            # Main Exception may occur from a non-updated version of chromedriver
            are_variables_set = set_global_variables()
        except GlobalVariablesNotSetException:
            # Another task
            is_chromedriver_updated = update_chromedriver()
            Log.info('set_global_variables, ' + str(MAX_START_ATTEMPTS - start_attempts) + ' attempts remaining')
            if is_chromedriver_updated:
                Log.info('chromedriver updated, trying to redefine global variables')
                are_variables_set = set_global_variables()
        finally:
            start_attempts += 1

    return are_variables_set


def set_global_variables():
    global initialized_driver

    f = open(os.getcwd() + "\\config.json", 'r')
    config = json.load(f)
    url = config['CALENDAR_URL']
    f.close()

    options = Options()
    # set it to True only in prod mode, hides the browser window and perform every operation in background
    options.headless = False
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # Assign to global variable the initialized driver instance.
        # This variable will be returned by main function
        initialized_driver = driver
        return True
    except (SessionNotCreatedException, WebDriverException, FileNotFoundError):
        Log.warn('Error occurred in driver initialization. Trying to retrieve an updated version of chromedriver...')
        raise GlobalVariablesNotSetException


def setup():
    Log.info('Starting setup operation')
    # Try to initialize global variables
    is_initialized = initialize_process()

    # If ChromeDriverUpdater terminated correctly, proceed with booking algorithm
    if is_initialized:
        Log.info('Instance correctly initialized')
        return initialized_driver
    else:
        Log.error('System failed to initialize session. check log for more info')

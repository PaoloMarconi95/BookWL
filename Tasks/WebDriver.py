from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# Custom
from Exceptions import GlobalVariablesNotSetException
from Tasks.ChromeDriverUpdater import update_chromedriver
import Log
import os
log = Log.logger


# Exported members
global_config = None

class WebDriver:

    def __init__(self):
        log.info('New instance of webdriver requested')


def get_driver():
    options = Options()
    # set it to True only in prod mode (Linux), hides browser window and perform every operation in background
    if os.name == 'nt':
        options.headless = False
    else:
        options.headless = True

    try:
        # Go to main booking page
        driver = webdriver.Chrome(options=options)
        return driver
    except (SessionNotCreatedException, WebDriverException, FileNotFoundError):
        log.warn('Error occurred in driver initialization')
        raise GlobalVariablesNotSetException
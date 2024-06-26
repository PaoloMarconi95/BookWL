from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from Exceptions import DriverNotInitializedException
from Config import LOGGER
import os


class WebDriverFactory:

    def get_driver(self):
        options = Options()
        # Made to turn off the webdriver bot detection
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False) 
        # set it to True only in prod mode (Linux), hides browser window and perform every operation in background
        if os.name == 'nt':
            options.headless = False
        else:
            options.headless = True

        try:
            # Go to main booking page
            driver = webdriver.Chrome(options=options)
            # Made to turn off the webdriver bot detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
            return driver
        except (SessionNotCreatedException, WebDriverException, FileNotFoundError) as e:
            LOGGER.warn(f"Error occurred in driver initialization: {e}")
            raise DriverNotInitializedException
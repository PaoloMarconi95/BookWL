from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
import subprocess

# Custom
from Exceptions import DriverNotInitializedException
from Tasks.ChromeDriverUpdater import update_chromedriver, get_latest_chromedriver_version
from Config import CONFIG, LOGGER
import os


class WebDriverFactory:

    def __init__(self):
        LOGGER.info('New instance of WebDriverFactory requested, checking if chromedriver is updated...')
        if not self.__is_driver_updated():
            update_chromedriver()


    def __is_driver_updated(self):
        last_verison = get_latest_chromedriver_version()
        check_installed_version_command = f"cd {CONFIG.chromedriver_folder} | chromedriver -v"
        installed_version = subprocess.check_output(check_installed_version_command, shell=True).decode()
        if last_verison in installed_version:
            return True
        else:
            return False

    def get_driver(self):
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
        except (SessionNotCreatedException, WebDriverException, FileNotFoundError) as e:
            LOGGER.warn(f"Error occurred in driver initialization: {e}")
            raise DriverNotInitializedException
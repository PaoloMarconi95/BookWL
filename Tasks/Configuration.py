# Standard
import json
import os
import datetime as dt
from datetime import datetime

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# Custom
from Exceptions import GlobalVariablesNotSetException
from Tasks.ChromeDriverUpdater import update_chromedriver
import Log
log = Log.logger

class Configuration:
    MAX_START_ATTEMPTS = 3

    def __init__(self):
        log.info('Starting config setup')
        # Try to initialize global variables
        if self.__initialize_process():
            log.info('Instance correctly initialized')
        else:
            log.error('System failed to initialize session. check log for more info')

    def __initialize_process(self):
        start_attempts = 1
        are_variables_set = False
        # Terminate the loop when variables are successfully set or max attempts are reached
        while (not are_variables_set) and (start_attempts <= Configuration.MAX_START_ATTEMPTS):
            try:
                # Main Exception may occur from a non-updated version of chromedriver
                are_variables_set = self.__set_global_variables()
            except GlobalVariablesNotSetException:
                # Another task
                is_chromedriver_updated = update_chromedriver()
                log.info('set_global_variables, ' + str(Configuration.MAX_START_ATTEMPTS - start_attempts) + ' attempts remaining')
                if is_chromedriver_updated:
                    log.info('chromedriver updated, trying to redefine global variables')
                    are_variables_set = self.__set_global_variables()
            finally:
                start_attempts += 1
        return are_variables_set

    # Setting main driver instance and configuration object
    def __set_global_variables(self):
        f = open(os.getcwd() + "\\config.json", 'r')
        data = json.load(f)
        f.close()
        self.config = Config(data)

        options = Options()
        # set it to True only in prod mode, hides the browser window and perform every operation in background
        options.headless = False
        try:
            # Go to main booking page
            self.driver = webdriver.Chrome(options=options)
            return True
        except (SessionNotCreatedException, WebDriverException, FileNotFoundError):
            log.warn('Error occurred in driver initialization. Trying to retrieve an updated version of chromedriver...')
            raise GlobalVariablesNotSetException

def get_closer_date_with_weekday(week_day):
    if not(0 < week_day < 7):
        log.error("tried to convert " + str(week_day) + " into week day")
        raise ValueError("Week Day " + str(week_day) + "Invalid!")
    else:
        today_week_day = datetime.today().weekday()
        delta = 7 - (today_week_day + (week_day - today_week_day))
        return datetime.today() + dt.timedelta(days=delta)

class Booking:

    def __init__(self, class_name, week_day):
        log.info('Starting booking setup')
        self.class_name = class_name
        self.date = get_closer_date_with_weekday(week_day)


class Config:

    def __init__(self, json_data):
        log.info('Starting Config setup')
        self.username = json_data["USERNAME"]
        self.password = json_data["PASSWORD"]
        self.signin_url = json_data["SIGNIN_URL"]
        self.calendar_url = json_data["CALENDAR_URL"]
        self.pipedream_mail_wf = json_data["PIPEDREAM_MAIL_WF"]

        # Bookings Creation
        self.bookings = []
        class_bookings = json_data["BOOKINGS"]
        log.info("adding bookings to config object")
        for booking in class_bookings:
            self.bookings.append((Booking(booking["CLASS_NAME"], booking["WEEK_DAY"])))



confFather = Configuration()

# Exported members
conf = confFather.config
driver = confFather.driver
bookings = conf.bookings

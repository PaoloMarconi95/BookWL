# Standard
import json
import os
import datetime as dt
from datetime import datetime
import pathlib

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
        self.signin_url = None
        self.calendar_url = None
        self.pipedream_mail = None
        self.users = []
        # Try to initialize global variables
        if self.__initialize_driver():
            json_data = self.__get_json_data()
            log.info('Instance correctly initialized, Starting Config setup')
            self.signin_url = json_data["SIGNIN_URL"]
            self.calendar_url = json_data["CALENDAR_URL"]
            self.pipedream_mail = json_data["PIPEDREAM_MAIL"]
            json_users = json_data["Users"]
            log.info("adding users to config object")
            for user in json_users:
                self.users.append(User(user))
        else:
            log.error('System failed to initialize session. check log for more info')


    def __initialize_driver(self):
        start_attempts = 1
        are_variables_set = False
        # Terminate the loop when variables are successfully set or max attempts are reached
        while (not are_variables_set) and (start_attempts <= Configuration.MAX_START_ATTEMPTS):
            try:
                # Main Exception may occur from a non-updated version of chromedriver
                are_variables_set = self.__set_driver()
            except GlobalVariablesNotSetException:
                # Another task
                is_chromedriver_updated = update_chromedriver()
                log.info('set_global_variables, ' + str(Configuration.MAX_START_ATTEMPTS - start_attempts) + ' attempts remaining')
                if is_chromedriver_updated:
                    log.info('chromedriver updated, trying to redefine global variables')
                    are_variables_set = self.__set_driver()
            finally:
                start_attempts += 1
        return are_variables_set


    def __set_driver(self):
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

    @classmethod
    def __get_json_data(cls):
        f = open(os.path.join(pathlib.Path(__file__).parent.parent.resolve(), "config.json"), 'r')
        data = json.load(f)
        f.close()
        return data


class Booking:
    def __init__(self, class_name, class_time, week_day):
        self.class_name = class_name
        self.class_time = class_time
        self.date = get_closer_date_with_weekday(week_day)


class User:
    def __init__(self, json_user):
        self.name = json_user["Name"]
        self.username = json_user["Username"]
        self.pwd = json_user["Pwd"]
        self.name = json_user["Name"]
        self.bookings = []
        json_bookings = json_user["Bookings"]
        log.info("adding bookings to config object")
        for booking in json_bookings:
            self.bookings.append((Booking(booking["CLASS_NAME"], booking["CLASS_TIME"], booking["WEEK_DAY"])))



def get_closer_date_with_weekday(week_day):
    if not(0 <= week_day <= 6):
        log.error("tried to convert " + str(week_day) + " into week day")
        raise ValueError("Week Day " + str(week_day) + "Invalid!")
    else:
        today_week_day = datetime.today().weekday()
        delta = 7 + (week_day - today_week_day)
        final_date = datetime.today() + dt.timedelta(days=delta)
        return datetime.strftime(final_date, "%d-%m-%Y")




# Exported members
global_config = Configuration()
driver = global_config.driver
users = global_config.users

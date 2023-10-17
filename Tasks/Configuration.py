# Standard
import json
import os
import datetime as dt
from datetime import datetime
import pathlib
import Log
log = Log.logger


# Exported members
global_config = None

class Configuration:
    MAX_START_ATTEMPTS = 3
    MAX_LOGIN_ATTEMPTS = 5

    def __init__(self):
        log.info('Starting config setup')
        self.signin_url = None
        self.calendar_url = None
        self.users = []
        self.driver = None
        json_data = self.__get_json_data()
        log.info('Instance correctly initialized, Starting Config setup')
        self.signin_url = json_data["SIGNIN_URL"]
        self.calendar_url = json_data["CALENDAR_URL"]
        self.gmail_key = json_data["GMAIL_KEY"]
        json_users = json_data["Users"]
        log.info("adding users to config object")
        for user in json_users:
            self.users.append(User(user))

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



def get_instance():
    global global_config
    if global_config is None:
        # Exported members
        global_config = Configuration()
        return global_config
    else:
        return global_config

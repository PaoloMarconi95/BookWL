import json
import time
import datetime as dt
from datetime import datetime
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

# noinspection PyPep8Naming
from Log import Log as LOG

MAX_ATTEMPTS = 20
PROCEDURE_START_AT = '17:18:10'
FIRE_START_AT = '17:22:59.999'
CLASS_TARGET = 'WEIGHTLIFTING 19.00'


def set_global_variables():
    global URL, driver, LOG

    f = open('config.json', 'r')
    config = json.load(f)
    URL = config['CALENDAR_URL']

    options = Options()
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    LOG = LOG('BookWL')
    LOG.info('Global variables set')


def start():
    login_el = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'FormLogin'))
    )
    if login_el is not None:
        login(login_el)
    else:
        time.sleep(5)

    # prepare the target for the fire
    set_date_to_next_week()
    LOG.info('Waiting for their backend to complete the date changing')
    time.sleep(8)  # date changes require some time for their backend

    # unleash the fire when the time's ready
    start_busy_wait()

    # let the fire extinguish
    time.sleep(20)

    # Check the registration success by clicking on ticket icon
    ticket_el = findWLbooking_el()
    ticket_el.click()
    time.sleep(4)
    book_completed = did_i_booked()

    # end of the process
    time.sleep(5)
    driver.close()

    if book_completed:
        mail_text = 'Booked WL Class for next week'
    else:
        mail_text = 'I was not able to book WL class for next week. Sorry :( :('

    send_me_an_email(mail_text)


def login(login_el):
    LOG.info('Logging in')
    f = open('config.json', 'r')
    config = json.load(f)
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    username_el.send_keys(config['Username'])
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    pwd_el.send_keys(config['Password'])
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    submit_el.click()
    LOG.info('Logged in')


def set_date_to_next_week():
    LOG.info('Setting date to next week')
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, 'AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom'))
    )
    date_of_today_plus_7 = ((dt.date.today()) + dt.timedelta(days=7)).strftime('%d-%m-%y')
    element.clear()
    element.send_keys(date_of_today_plus_7)


def findWLbooking_el():
    span_inner_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + CLASS_TARGET + "']"))
    )
    outer_el = span_inner_el.find_element(By.XPATH, '../../..')
    booking_el = outer_el.find_element(By.XPATH, ".//a[@title='Reserve spot in class']")
    return booking_el


def start_busy_wait():
    finish = False
    clicks = 0
    LOG.info('Waiting for fire to start')
    while not finish:
        now = datetime.now().time()

        if now >= datetime.strptime(FIRE_START_AT, '%H:%M:%S.%f').time():
            refresh_page()
            wl_booking_el = findWLbooking_el()
            LOG.info('Fire started at ' + str(datetime.now().time()))
            while not finish:
                wl_booking_el.click()
                clicks += 1
                if clicks > MAX_ATTEMPTS:
                    finish = True
                    LOG.info('reached the maximum number of attempts at ' + str(datetime.now().time()))

        time.sleep(1)


def did_i_booked():
    try:
        fdb_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'Feedback_Message_Text'))
        )
        text_found = fdb_element.text.rstrip().lower()
        if text_found == 'Reservation Confirmed'.lower() or \
                text_found == 'You have a reservation for this class'.lower():
            LOG.info('Found the correct ticket icon with the correct text')
            return True
        else:
            LOG.error('Found the correct ticket icon without the correct text')
            LOG.error('The text found was ' + str(text_found))
            return False
    except:
        LOG.error('Didn\'t found the correct ticket in 10 seconds')
        return False


def send_me_an_email(message):
    url = 'https://da897d59ec3093f998d930d05ceb60e4.m.pipedream.net'
    msg = {'message': message}
    requests.post(url, data=msg)


def refresh_page():
    LOG.info('Refreshing page')
    driver.get(URL)
    driver.refresh()


if __name__ == '__main__':
    set_global_variables()
    time_to_start = False
    while not time_to_start:
        if datetime.now().time() >= datetime.strptime(PROCEDURE_START_AT, '%H:%M:%S').time():
            time_to_start = True
            LOG.info('Starting the procedure')
            start()
        time.sleep(10)

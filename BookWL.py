import json
import time
import datetime as dt
from datetime import datetime
import requests
from selenium.common.exceptions import NoSuchElementException, TimeoutException, SessionNotCreatedException

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

# noinspection PyPep8Naming
from Log import Log as LOG

MAX_ATTEMPTS = 30
PROCEDURE_START_AT = '18:58:00'
FIRE_START_AT = '18:59:57'
CLASS_TARGET = 'WEIGHTLIFTING 19.00'


def set_global_variables():
    global URL, driver, LOG

    f = open('config.json', 'r')
    config = json.load(f)
    URL = config['CALENDAR_URL']

    options = Options()
    # options.headless = True
    try:
        driver = webdriver.Chrome(options=options)
    except SessionNotCreatedException as exc:
        LOG.warn('Error occurred in driver initialization. Trying to retrieve an updated version of chromedriver...')
        print(str(exc))
    driver.get(URL)
    LOG = LOG('BookWL')
    LOG.info('Global variables set')
    f.close()


def start():
    try:
        login_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'FormLogin'))
        )
        login(login_el)
    except TimeoutException:
        time.sleep(5)

    # prepare the target for the fire
    set_date_to_next_week()
    LOG.info('Waiting for their backend to complete the date changing')
    time.sleep(8)  # date changes require some time for their backend

    # unleash the fire when the time's ready
    is_book_completed = book_class()

    # end of the process
    time.sleep(5)
    driver.close()

    if is_book_completed:
        LOG.info('Successfully booked ' + CLASS_TARGET)
        mail_text = 'Booked WL Class for next week'
    else:
        LOG.error('Class not booked!!')
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
    f.close()


def get_row_class_target():
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + CLASS_TARGET + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    return wl_class_row


def set_date_to_next_week():
    LOG.info('Setting date to next week')
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, 'AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom'))
    )
    date_of_today_plus_7 = ((dt.date.today()) + dt.timedelta(days=7)).strftime('%d-%m-%y')
    element.clear()
    element.send_keys(date_of_today_plus_7)


def find_booking_el_and_class_row():
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + CLASS_TARGET + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    booking_el = wl_class_row.find_element(By.XPATH, ".//a[@title='Make Reservation']")
    return booking_el


def book_class():
    finish = False
    success = False
    clicks, tries = 0, 0
    LOG.info('Waiting for fire to start')
    while not finish:
        now = datetime.now().time()

        if now >= datetime.strptime(FIRE_START_AT, '%H:%M:%S').time():
            LOG.info('Fire started')
            while not finish:
                driver.refresh()
                try:
                    tries += 1
                    wl_booking_el = find_booking_el_and_class_row()
                    wl_booking_el.click()
                    clicks += 1
                except NoSuchElementException:
                    LOG.info('Make Reservation title not found, could be already booked or not opened yet')
                    if tries > MAX_ATTEMPTS:
                        finish = True
                        LOG.info('reached the maximum number of attempts')
                    if find_ticket_icon():
                        finish = True
                        success = True
                        LOG.info('Booked after ' + str(clicks) + ' clicks')

        time.sleep(0.5)

    return success


def find_ticket_icon():
    span_inner_el = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='" + CLASS_TARGET + "']"))
    )
    wl_class_row = span_inner_el.find_element(By.XPATH, '../../..')
    try:
        wl_class_row.find_element(By.CSS_SELECTOR, '.icon.icon-ticket')
        return True
    except NoSuchElementException:
        LOG.info('Didn\'t find icon svg')
        return False


def send_me_an_email(message):
    url = 'https://da897d59ec3093f998d930d05ceb60e4.m.pipedream.net'
    msg = {'message': message}
    requests.post(url, data=msg)


if __name__ == '__main__':
    global driver
    set_global_variables()
    time_to_start = False
    while not time_to_start:
        if datetime.now().time() >= datetime.strptime(PROCEDURE_START_AT, '%H:%M:%S').time():
            time_to_start = True
            LOG.info('Starting the procedure')
            try:
                start()
            except Exception as e:
                LOG.error(str(e.__class__) + ' : ' + str(e))
                driver.close()
        time.sleep(10)

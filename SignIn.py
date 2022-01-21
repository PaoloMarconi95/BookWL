import json
import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from Exceptions import NoReservationFoundException, ClassNotFoundWithinDropDownException


def start():
    set_global_variables()

    # Set page to calendar
    driver.get(CALENDAR_URL)

    login_el = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'FormLogin'))
    )
    if login_el is not None:
        login(login_el)
    else:
        time.sleep(5)

    class_reserved = reservation_for_today()
    print('class reserved : ' + str(class_reserved))

    # Change page to signin
    driver.get(SIGNIN_URL)

    # set correct class and sign in
    set_correct_class_for_dropdown(class_reserved)
    sign_in()

    # end of the process
    time.sleep(2)
    driver.close()


def set_global_variables():
    global SIGNIN_URL, CALENDAR_URL, driver
    options = Options()
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    f = open('config.json', 'r')
    config = json.load(f)
    SIGNIN_URL = config['SIGNIN_URL']
    CALENDAR_URL = config['CALENDAR_URL']


def login(login_el):
    print('Logging in at ' + str(datetime.now().time()))
    f = open('config.json', 'r')
    config = json.load(f)
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    username_el.send_keys(config['Username'])
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    pwd_el.send_keys(config['Password'])
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    submit_el.click()


def reservation_for_today():
    driver.get(CALENDAR_URL)
    daily_classes = get_every_class_of_today()
    print('got every classes')
    class_reserved = search_for_ticket_icon_within(daily_classes)

    if class_reserved is None:
        raise NoReservationFoundException('No reservation Found for today')
    else:
        return class_reserved


def search_for_ticket_icon_within(daily_classes):
    today_reservation = None
    for class_entry in daily_classes:
        try:
            booked_class = class_entry.find_element(By.CLASS_NAME, 'icon-ticket')
            if booked_class is not None:
                today_reservation = class_entry.find_element(By.TAG_NAME, 'span').get_attribute('title')
        except NoSuchElementException:
            pass
    return today_reservation


def get_every_class_of_today():
    table_el = driver.find_element(By.ID, 'AthleteTheme_wt6_block_wtMainContent_wt9_wtClassTable')
    tbody_el = table_el.find_element(By.TAG_NAME, 'tbody')
    every_tr = tbody_el.find_elements(By.TAG_NAME, 'tr')
    classes = []
    for tr in every_tr:
        if tr.get_attribute('style') != '':
            classes.append(tr)
        if tr.get_attribute('style') == '' and len(classes) > 0:
            return classes


def set_correct_class_for_dropdown(class_name):
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'))
    )
    all_options = dropdown.find_elements(By.TAG_NAME, 'option')
    correctly_set = False
    for option in all_options:
        if option.text == class_name:
            option.click()
            correctly_set = True

    if not correctly_set:
        raise ClassNotFoundWithinDropDownException(class_name)


def sign_in():
    signin_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtSubNavigation_wtSignInButton2'))
    )
    signin_button.click()


def refresh_page(url):
    driver.get(url)
    driver.refresh()


if __name__ == '__main__':
    start()

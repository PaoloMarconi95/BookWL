import json
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import datetime

driver = webdriver.Edge()
driver.get("https://app.wodify.com/Schedule/CalendarListViewEntry.aspx")


def start():
    login_el = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "FormLogin"))
    )
    if login_el is not None:
        login(login_el)

    set_date_to_next_week()
    time.sleep(10)
    wl_booking_el = findWLbooking_el()

    # start the loop

    wl_booking_el.click()

    time.sleep(3)

    driver.close()


def login(login_el):
    # Opening JSON file
    f = open('config.json', 'r')
    config = json.load(f)
    username_el = login_el.find_element(By.ID, "Input_UserName")
    username_el.send_keys(config["Username"])
    pwd_el = login_el.find_element(By.ID, "Input_Password")
    pwd_el.send_keys(config["Password"])
    submit_el = login_el.find_element(By.TAG_NAME, "button")
    submit_el.click()


def set_date_to_next_week():
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, "AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom"))
    )
    # date_of_today_plus_7 = ((datetime.date.today()) + datetime.timedelta(days=7)).strftime('%d-%m-%y')
    date_of_today_plus_7 = (datetime.date.fromisoformat("2021-11-22") + datetime.timedelta(days=7)).strftime('%d-%m-%y')
    element.clear()
    element.send_keys(date_of_today_plus_7)

def findWLbooking_el():
    print("cerco wl el")
    span_inner_el = driver.find_element(By.XPATH, "//span[@title='WEIGHTLIFTING 19.00']")
    outer_el = span_inner_el.find_element(By.XPATH, '../../..')
    print(str(outer_el))
    wl_booking_el = outer_el.find_element(By.XPATH, "//a[@title='Reserve spot in class']")
    return wl_booking_el



if __name__ == "__main__":
    start()

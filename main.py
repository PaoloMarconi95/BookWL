import json

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

    booking_el = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, "AthleteTheme_wt6_block_wtMainContent_wt9_wtClassTable_ctl13_wtAddReservationLink2"))
    )
    booking_el.click()
    driver.implicitly_wait(4)

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
    date_of_today_plus_7 = ((datetime.date.today()) + datetime.timedelta(days=7)).strftime('%d-%m-%y')
    element.clear()
    element.send_keys(date_of_today_plus_7)


if __name__ == "__main__":
    start()

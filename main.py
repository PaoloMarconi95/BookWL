import json
import time
import datetime as dt
from datetime import datetime
import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Edge()
driver.get("https://app.wodify.com/Schedule/CalendarListViewEntry.aspx")


def start():
    login_el = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "FormLogin"))
    )
    if login_el is not None:
        login(login_el)

    # prepare the target for the fire
    set_date_to_next_week()
    time.sleep(10)
    wl_booking_el = findWLbooking_el()

    # unleash the fire
    start_busy_wait(wl_booking_el)

    # let the fire extinguish
    time.sleep(15)

    # check the damage
    wl_booking_el = findWLbooking_el()
    wl_booking_el.click()
    book_completed = did_I_booked()

    # end of the process
    time.sleep(3)
    driver.close()

    mail_text = ""
    if book_completed:
        mail_text = "Booked WL Class for next week"
    else:
        mail_text = "I was not able to book WL class for nextr week.\nSorry :( :("

    send_me_an_email(mail_text)


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
    date_of_today_plus_7 = ((dt.date.today()) + dt.timedelta(days=7)).strftime('%d-%m-%y')
    #date_of_today_plus_7 = (dt.date.fromisoformat("2021-11-22") + dt.timedelta(days=7)).strftime('%d-%m-%y')
    element.clear()
    element.send_keys(date_of_today_plus_7)


def findWLbooking_el():
    print("cerco wl el")
    span_inner_el = driver.find_element(By.XPATH, "//span[@title='WEIGHTLIFTING 19.00']")
    outer_el = span_inner_el.find_element(By.XPATH, '../../..')
    print(str(outer_el))
    wl_booking_el = outer_el.find_element(By.XPATH, "//a[@title='Reserve spot in class']")
    return wl_booking_el


def start_busy_wait(wl_booking_el):
    finish = False
    count = 0

    while not finish:
        now = datetime.now().time()
        if now >= datetime.strptime('19:00:00', '%H:%M:%S').time():

            while not finish:
                wl_booking_el.click()
                count += 1
                if count > 50:
                    finish = True
                time.sleep(0.5)

        time.sleep(3)


def did_I_booked():
    fdb_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "Feedback_Message_Text"))
    )
    if fdb_element.text == "You have a reservation for this class":
        return True
    else:
        return False

def send_me_an_email(message):
    url = "https://da897d59ec3093f998d930d05ceb60e4.m.pipedream.net"
    msg = {'message': message}

    x = requests.post(url, data=msg)
    print(x.text)



if __name__ == "__main__":
    start()

# Standard
import json
from datetime import datetime
import os

# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Custom
from Log import Log
Log = Log.get_instance()


def signin(driver):
    login_el = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'FormLogin'))
    )
    Log.info("Logging in at " + str(datetime.now().time()))
    f = open(os.getcwd() + "\\config.json", 'r')
    config = json.load(f)
    username_el = login_el.find_element(By.ID, 'Input_UserName')
    username_el.send_keys(config['Username'])
    pwd_el = login_el.find_element(By.ID, 'Input_Password')
    pwd_el.send_keys(config['Password'])
    submit_el = login_el.find_element(By.TAG_NAME, 'button')
    submit_el.click()
    Log.info('Logged in')

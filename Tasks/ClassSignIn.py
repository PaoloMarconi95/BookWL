# Standard
from datetime import datetime
import time

# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

# Custom
import Log
import Tasks.Configuration as Configuration
from Exceptions import ClassNotFoundWithinDropDownException
from Tasks.Booking import get_booked_classes_for_date

config = Configuration.global_config
driver = Configuration.driver
log = Log.logger


def get_booked_class_for_current_time():
    booked_class = get_booked_classes_for_date(datetime.strftime(datetime.today(), "%d-%m-%Y"))
    if booked_class is not None:
        # Parse the element text
        booked_class = booked_class.text.split('\n')[0]
        name = [char for char in booked_class if (char.isalpha() or char == ' ')]
        name = ''.join(name).strip()
        log.info(f'ho trovato questa classe con una prenotazione: {name}')
        return name
    else:
        log.info('Non ho trovato nessuna classe prenotata per oggi a quest\'ora')


def set_correct_program(class_name):
    settings_accordion = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'settingsCollapsibleHeader'))
    )
    settings_accordion.click()
    time.sleep(1)
    program_dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtSubNavigation_wtProgram_Input'))
    )
    select = Select(program_dropdown)
    all_options = select.options
    correctly_set = False
    for index, option in enumerate(all_options):
        option_text = option.get_attribute("innerText").upper()
        if class_name.upper() in option_text:
            select.select_by_index(index)
            correctly_set = True
    if not correctly_set:
        raise ClassNotFoundWithinDropDownException(class_name)


def set_correct_time():
    time_dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'))
    )
    select = Select(time_dropdown)
    all_options = select.options
    correctly_set = False
    for index, option in enumerate(all_options):
        option_text = option.get_attribute("innerText")
        if datetime.strftime(datetime.today(), "%H") in option_text:
            select.select_by_index(index)
            correctly_set = True
    if not correctly_set:
        raise ClassNotFoundWithinDropDownException(datetime.strftime(datetime.today(), "%H"))


def sign_in(class_name):
    driver.get(config.signin_url)
    log.info('Setting correct program from dropdown')
    set_correct_program(class_name)
    log.info('Setting correct time from dropdown')
    set_correct_time()
    log.info('Looking for sign-in button')
    sign_in_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtSubNavigation_wtSignInButton2'))
    )
    sign_in_button.click()

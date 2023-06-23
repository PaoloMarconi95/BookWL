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
import Configuration
from Exceptions import ClassNotFoundWithinDropDownException
from Tasks.Booking import get_booked_class_and_program_for_date

config = Configuration.get_instance()
driver = config.driver
log = Log.logger


def get_booked_class_and_program_for_current_time():
    booked_class_el = get_booked_class_and_program_for_date(datetime.strftime(datetime.today(), "%d-%m-%Y"))
    if booked_class_el is not None:
        # Parse the element text
        booked_class = booked_class_el.text.split('\n')[0]
        booked_program = booked_class_el.text.split('\n')[3]
        log.info(f'Found that class {booked_class} was booked for current datetime')
        return booked_class, booked_program
    else:
        log.info('No class found for current datetime')
        return None, None

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


def set_correct_class(class_name):
    time_dropdown = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'))
    )
    select = Select(time_dropdown)
    select.select_by_visible_text(class_name)


def sign_in(class_name, class_program):
    driver.get(config.signin_url)
    time.sleep(2)
    log.info('Setting correct program from dropdown')
    set_correct_program(class_program)
    time.sleep(2)
    log.info('Setting correct time from dropdown')
    set_correct_class(class_name)
    log.info('Looking for sign-in button')
    driver.refresh()
    time.sleep(2)
    sign_in_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'AthleteTheme_wtLayout_block_wtSubNavigation_wtSignInButton2'))
    )
    log.info('Sign in button found')
    sign_in_button.click()

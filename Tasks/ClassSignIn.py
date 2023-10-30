# Standard
from datetime import datetime
import time

# Selenium
from selenium.webdriver.support.ui import Select

# Custom
from Config import CONFIG, LOGGER
from Exceptions import ClassNotFoundWithinDropDownException
from Tasks.SafeAccess import safe_access_by_id
from Tasks.Booking import get_booked_class_and_program_for_date

TIME_DROPDOWN_ID = 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'
PROGRAM_DROPDOWN_ID = 'AthleteTheme_wtLayout_block_wtSubNavigation_wtProgram_Input'
SIGNIN_BUTTON_ID = 'AthleteTheme_wtLayout_block_wtSubNavigation_wtSignInButton2'
SETTINGS_ACCORDION_ID = 'settingsCollapsibleHeader'


def get_booked_class_and_program_for_current_time(wd):
    booked_class_el = get_booked_class_and_program_for_date(datetime.strftime(datetime.today(), "%d-%m-%Y"), wd)
    if booked_class_el is not None:
        # Parse the element text
        booked_class = booked_class_el.text.split('\n')[0]
        booked_program = booked_class_el.text.split('\n')[3]
        LOGGER.info(f'Found that class {booked_class} was booked for current datetime')
        return booked_class, booked_program
    else:
        LOGGER.info('No class found for current datetime')
        return None, None


def set_correct_program(class_name, wd):
    settings_accordion = safe_access_by_id(wd, SETTINGS_ACCORDION_ID)
    settings_accordion.click()
    time.sleep(1)
    program_dropdown = safe_access_by_id(wd, PROGRAM_DROPDOWN_ID)
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


def set_correct_class(class_name, wd):
    time_dropdown = safe_access_by_id(wd, TIME_DROPDOWN_ID)
    select = Select(time_dropdown)
    select.select_by_visible_text(class_name)


def sign_in(class_name, class_program, wd):
    wd.get(CONFIG.signin_url)
    LOGGER.info('Setting correct program from dropdown')
    set_correct_program(class_program, wd)
    time.sleep(1)
    LOGGER.info('Setting correct time from dropdown')
    set_correct_class(class_name, wd)
    LOGGER.info('Looking for sign-in button')
    wd.refresh()
    sign_in_button = safe_access_by_id(wd, SIGNIN_BUTTON_ID)
    LOGGER.info('Sign in button found')
    sign_in_button.click()
    LOGGER.info('And clicked!')

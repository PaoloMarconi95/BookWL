# Selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Exceptions import ClassNotFoundWithinDropDownException
# Custom
import Log
import Configuration

driver = Configuration.driver
log = Log.logger


def set_correct_class_for_dropdown(class_name):
    log.info('Looking for dropdown')
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'))
    )
    all_options = dropdown.find_elements(By.TAG_NAME, 'option')
    correctly_set = False
    for option in all_options:
        if option.text == class_name:
            log.info(Log, 'Found correct value')
            option.click()
            correctly_set = True

    if not correctly_set:
        raise ClassNotFoundWithinDropDownException(class_name)

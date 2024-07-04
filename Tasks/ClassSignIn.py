# Standard
import time

# Custom
from Config import CONFIG, LOGGER
from Model.CrossFitClass import CrossFitClass
from Model.BrowserProvider import BrowserProvider

PROGRAM_DROPDOWN_ID = 'AthleteTheme_wtLayout_block_wtSubNavigation_wtProgram_Input'
CLASS_DROPDOWN_ID = 'AthleteTheme_wtLayout_block_wtMainContent_wtClass_Input'
SIGNIN_BUTTON_ID = 'AthleteTheme_wtLayout_block_wtSubNavigation_wtSignInButton2'


def sign_in(crossfit_class: CrossFitClass, browser_provider: BrowserProvider):
    browser_provider.change_url(CONFIG.signin_url, f"#AthleteTheme_wtLayout_block_wtSubNavigation_wtSignMeIn")
    LOGGER.info('Setting correct program from dropdown')
    browser_provider.page.locator(f"#settingsCollapsibleHeader").nth(0).click()
    time.sleep(2)
    program_dropdown = browser_provider.page.locator(f"#{PROGRAM_DROPDOWN_ID}")
    program_dropdown.select_option(label=crossfit_class.program)
    time.sleep(2)
    LOGGER.info('Setting correct class from dropdown')
    class_dropdown = browser_provider.page.locator(f"#{CLASS_DROPDOWN_ID}")
    class_dropdown.select_option(label=crossfit_class.name)
    LOGGER.info('Looking for sign-in button')
    time.sleep(2)
    browser_provider.page.locator(f"#{SIGNIN_BUTTON_ID}").nth(0).click()
    LOGGER.info('Clicked sign in button!')
    time.sleep(5)

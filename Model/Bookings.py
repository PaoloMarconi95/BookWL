# Playwright
from playwright.sync_api import Locator

# Standard
import time
from datetime import datetime, timedelta, date
import re

# Custom
from Config import CONFIG
from Model.CrossFitClass import CrossFitClass
from Model.BrowserProvider import BrowserProvider


class Bookings:
    def __init__(self, bp: BrowserProvider):
        self.browser_provider: BrowserProvider = bp
        self.class_rows: dict[datetime.date, list[Locator]] = {}
        self.crossfit_classes: dict[datetime.date, list[CrossFitClass]] = {}

    def compute_bookings_for_date(self, date: date = None) -> None:
        self.browser_provider.change_url(CONFIG.calendar_url, f"#{CONFIG.calendar_el_id}")
        if date is not None:
            self.set_calendar_date(date)

        classes = self.browser_provider.page.locator('//table/tbody/tr')
        parsed_date = None
        for i in range(1, classes.count()):
            cls = classes.nth(i)
            if is_title_row(cls):
                parsed_date = get_title_date_from_row(cls)
                self.crossfit_classes[parsed_date] = []
                self.class_rows[parsed_date] = []
            elif is_booking_row(cls):
                if parsed_date is not None:
                    self.class_rows[parsed_date].append(cls)
                    c_class = get_class_from_row(cls, parsed_date)
                    self.crossfit_classes[parsed_date].append(c_class)
                else:
                    raise RuntimeError("Booking row found without previous title (weekday + date)")

    def set_calendar_date(self, date: date) -> None:
        date_str = date.strftime('%d-%m-%Y')
        self.browser_provider.page.fill(
            '#AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom', " ")
        time.sleep(0.5)
        self.browser_provider.page.fill(
            '#AthleteTheme_wt6_block_wtMainContent_wt9_W_Utils_UI_wt216_block_wtDateInputFrom', date_str)
        time.sleep(2)

    def get_booked_classes_within_minutes(self, minutes: int = None) -> list[CrossFitClass]:
        classes = []
        datetime_n_minutes_ahead = datetime.now() + timedelta(minutes=minutes)
        for date_classes in self.crossfit_classes.values():
            for cls in date_classes:
                if cls.is_booked and not cls.is_waitlisted and datetime_n_minutes_ahead > cls.datetime > datetime.now():
                    classes.append(cls)
        return classes


def get_class_from_row(cl: Locator, date: date) -> CrossFitClass:
    text = cl.inner_text().replace('\t', '').split('\n')
    text = [entry for entry in text if entry != ""]
    is_forbidden_icon_present = cl.locator('svg.icon.icon-forbidden').count() > 0
    is_ticket_icon_present = cl.locator('svg.icon.icon-ticket').count() > 0
    is_waitlisted = is_forbidden_icon_present and not is_ticket_icon_present
    # Standard case
    if len(text) == 6:
        class_datetime = datetime(year=date.year, month=date.month, day=date.day, hour=int(text[4][:2]), minute=int(text[4][3:]))
        return CrossFitClass(name=text[0], datetime=class_datetime, program=text[3],
                             is_booked=is_ticket_icon_present, is_waitlisted=is_waitlisted)
    # Yoga case
    elif len(text) == 5:
        class_datetime = datetime(year=date.year, month=date.month, day=date.day, hour=int(text[3][:2]), minute=int(text[3][3:]))
        return CrossFitClass(name=text[0], datetime=class_datetime, program=text[2],
                             is_booked=is_ticket_icon_present, is_waitlisted=is_waitlisted)
    else:
        raise RuntimeError(f"Found a class that does not have 6 entries: {cl.inner_text()}")


def get_title_date_from_row(cl: Locator) -> date:
    text = cl.inner_text().replace('\n', '')
    text = text.replace('\t', '')
    pattern = '(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-20\\d{2}'
    date_string = re.search(pattern, text).group()
    return datetime.strptime(date_string, '%d-%m-%Y').date()


def is_title_row(cl: Locator) -> bool:
    text = cl.inner_text().replace('\n', '')
    text = text.replace('\t', '')

    pattern = '(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-20\\d{2}'
    if re.search(pattern, text):
        return True
    else:
        return False


def is_booking_row(cl: Locator) -> bool:
    if cl.get_attribute('style') == 'font-size: 0.75em':
        return True
    else:
        return False

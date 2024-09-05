from datetime import datetime

# Custom
from Config.Configuration import User
from Model.Bookings import Bookings
from Model.BrowserProvider import BrowserProvider
from Tasks.SendEmail import send_email
from Tasks.ClassSignIn import sign_in
from Config import LOGGER, CONFIG


def sign_in_to_booked_class(user: User, bp: BrowserProvider) -> None:
    now = datetime.now()
    LOGGER.info(f"Starting sign-in process for user {str(user.name)} and date {now}")
    bookings = Bookings(bp)
    bookings.compute_bookings_for_datetime(date=now)
    booked_classes = bookings.get_booked_classes_within_minutes(minutes=20)

    if len(booked_classes) > 1:
        LOGGER.error(f"Found more than 1 class booked for user {str(user.name)} with a 20 minutes neighborhood")

    if len(booked_classes) == 1:
        LOGGER.info(f"Found 1 class booked for user {str(user.name)}. Starting sign in")
        sign_in(booked_classes[0], bp)
        LOGGER.info(f"Sign in completed")
        send_email(user.mail, "Auto SignIn", f"Correctly signed in for class {booked_classes[0].name}")

    if len(booked_classes) == 0:
        LOGGER.info(f"No booked class found! Terminating program...")


if __name__ == "__main__":
    try:
        for usr in CONFIG.users:
            browser_provider = BrowserProvider(usr)
            sign_in_to_booked_class(usr, browser_provider)
            browser_provider.dispose()
    except Exception as main_exception:
        LOGGER.error(main_exception)
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        LOGGER.info('Program terminated')

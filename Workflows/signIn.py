import time
from datetime import datetime

# Custom
from DB.Entities.User import User
from Model.Booking import Bookings
from Model.BrowserProvider import BrowserProvider
from Tasks.SendEmail import send_email
from Tasks.ClassSignIn import sign_in
from Config import LOGGER


def sign_in_to_booked_class(user: User, bp: BrowserProvider):
    now = datetime.now()
    LOGGER.info(f"Starting sign-in process for user {str(user.name)} and date {now}")
    bookings = Bookings(bp)
    bookings.compute_bookings(date=now)
    booked_classes = bookings.get_booked_classes_within_minutes(minutes=20)

    if len(booked_classes) > 1:
        LOGGER.error(f"Found more than 1 class booked for user {str(user.name)} with a 20 minutes neighborhood")

    if len(booked_classes) == 1:
        LOGGER.info(f"Found 1 class booked for user {str(user.name)}. Starting sign in")
        sign_in(booked_classes[0], bp)
        LOGGER.info(f"Sign in completed")
        send_email(user.mail, "Auto SignIn", f"Correctly signed in for class {booked_classes[0].name}")


if __name__ == "__main__":
    try:
        users = User.get_every_users()
        #users = [User(id=0, name='Paolo', mail='paolomarconi1995@gmail.com', password='Internet0Cross')]
        for user in users:
            bp = BrowserProvider(user)
            sign_in_to_booked_class(user, bp)
            bp.page.close()
            bp.browser.close()
    except Exception as main_exception:
        LOGGER.error("FATAL")
        LOGGER.error(main_exception)
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        LOGGER.info('Program terminated')

import time
from datetime import datetime

from Model.Booking import Bookings
from Model.BrowserProvider import BrowserProvider
from Tasks.SendEmail import send_email
from Config import LOGGER
from DB.Entities.User import User
import multiprocessing as mp
import traceback
import sys
from Config import CONFIG


def error_handler(ex: BaseException) -> None:
    exception = traceback.format_exception(type(ex), ex, ex.__traceback__)
    ex_info = sys.exc_info()
    LOGGER.error(f"An error occurred in booking_sign_in thread.\n{str(ex)}")
    send_email("paolomarconi1995@gmail.com", "Scan booked class Error",
               f"Exception: {str(ex)}\nTraceback:\n{str(exception)}\nInfo:\n{ex_info}")


def upsert_every_booked_class(user: User, bp: BrowserProvider):
    LOGGER.info("Starting sign-in process for user " + str(user.name))
    bookings = Bookings(bp)
    bookings.compute_bookings(datetime.now())


    # if user.is_logged_in:
    #     current_hour = datetime.strftime(datetime.today(), "%H")
    #     next_hour = datetime.strftime(datetime.today() + timedelta(hours=1), "%H")
    #     classes = []
    #     # See If there's a class in current hour (it's 8 and class at 8:15 for example, rarely happens)
    #     classes.append(get_booked_crossfit_class_for_time(webdriver, current_hour))
    #     # See If there's a class in current hour (it's 17 and class at 18)
    #     classes.append(get_booked_crossfit_class_for_time(webdriver, next_hour))
    #     for crossfit_class in [c_class for c_class in classes if c_class is not None]:
    #         crossfit_class_id = crossfit_class.upsert()
    #         booking = Booking(user_id=user.id, class_id=crossfit_class_id)
    #         booking.upsert()
    #     user.log_out(webdriver)
    # else:
    #     LOGGER.error(f'Login for user {user.name} failed!')
    #     send_email(user.mail, "Login Fallito!",
    #                f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")


def main():
    users = User.get_every_users()
    users = [User(id=0, name='Paolo', mail='paolomarconi1995@gmail.com', password='Internet0Cross')]  # Debug
    for user in users:
        bp = BrowserProvider()
        upsert_every_booked_class(user, bp)


if __name__ == "__main__":
    try:
        main()
    except Exception as main_exception:
        LOGGER.error("FATAL")
        LOGGER.error(main_exception)
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        LOGGER.info('Program terminated')

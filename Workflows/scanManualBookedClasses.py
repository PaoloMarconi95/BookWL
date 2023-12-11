from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_crossfit_class_for_time
from Tasks.SendEmail import send_email
import traceback
from threading import Thread
from Config import CONFIG, LOGGER
from Workflows import WEBDRIVERFACTORY
from DB.Entities.Booking import Booking
from DB.Entities.User import User
from DB.Entities.CrossFitClass import CrossFitClass
from datetime import datetime
from multiprocessing.pool import ThreadPool

def error_handler(ex):
    LOGGER.error(f"An error occurred in booking_sign_in thread.\n{str(ex)}")
    send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(ex))


def main_thread_work(user: User, webdriver):
    LOGGER.info("Starting sign-in process for user " + str(user.name))
    logged_in = False
    attempts = 0
    while not logged_in and attempts < CONFIG.max_login_attempts:
        try:
            logged_in = login(user, webdriver)
        except AttributeError as e:
            LOGGER.error(f'Login for user {user.name} failed! ({e}) Trying again...')
        finally:
            attempts += 1

    if logged_in:
        current_hour = int(datetime.strftime(datetime.today(), "%H"))
        classes = []
        # See If there's a class in current hour (it's 8 and class at 8:15 for example, rarely happens)
        classes.append(get_crossfit_class_for_time(webdriver, str(current_hour)))
        # See If there's a class in current hour (it's 17 and class at 18)
        classes.append(get_crossfit_class_for_time(webdriver, str(current_hour + 1)))
        for crossfit_class in [c_class for c_class in classes if c_class is not None]:
            crossfit_class_id = crossfit_class.upsert()
            booking = Booking(user_id=user.id, class_id=crossfit_class_id, is_signed_in=False)
            booking.upsert()
        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.name, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    webdriver_to_be_closed = []
    users = User.get_every_users()
    with ThreadPool() as pool:
        for user in users:
            webdriver = WEBDRIVERFACTORY.get_driver()
            webdriver_to_be_closed.append(webdriver)
            pool.apply_async(main_thread_work, args=(user, webdriver), error_callback=error_handler)
        pool.close()
        pool.join()
    
    for wb in webdriver_to_be_closed:
        wb.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as main_exception:
        LOGGER.error(f"FATAL")
        LOGGER.error(main_exception)
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        LOGGER.info('Program terminated')

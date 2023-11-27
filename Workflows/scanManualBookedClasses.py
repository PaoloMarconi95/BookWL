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
from datetime import timedelta, datetime


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
        current_hour = str(int(datetime.strftime(datetime.today(), "%H")))
        classes = []
        classes.append(get_crossfit_class_for_time(webdriver, current_hour))
        classes.append(get_crossfit_class_for_time(webdriver, str(int(current_hour) + 1)))
        for crossfit_class in classes:
            if crossfit_class is not None and not crossfit_class.exists():
                LOGGER.info(f"Found that class {crossfit_class} does not exists within db! inserting it...")
                crossfit_class_id = CrossFitClass.create_crossfit_class(crossfit_class)
                booking_time = - timedelta(hours=int(crossfit_class.time.split(':')[0]), minutes=int(crossfit_class.time.split(':')[1]), ) \
                        - timedelta(minutes=CONFIG.sign_in_delta)
                # [:-3] to transform from 00:10:00 to 00:10
                Booking.create_booking(Booking(
                    user_id=user.id, class_id=crossfit_class_id, 
                    time=str(booking_time)[:-3], is_signed_in=False))
                LOGGER.info(f"Class {crossfit_class} succesfully inserted!")
        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.name, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    users = User.get_every_users()
    threads = []
    for user in users:
        webdriver = WEBDRIVERFACTORY.get_driver()
        t = Thread(target=main_thread_work, args=(user, webdriver))
        t.start()
        threads.append((t, webdriver))

    for t, wb in threads:
        t.join()
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

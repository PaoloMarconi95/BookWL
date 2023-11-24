from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import sign_in
from Tasks.SendEmail import send_email
import traceback
from threading import Thread
from Config import CONFIG, LOGGER
from Workflows import WEBDRIVERFACTORY
from DB.Entities.Booking import Booking
from DB.Entities.User import User
from DB.Entities.CrossFitClass import CrossFitClass

def booking_sign_in(booking: Booking, webdriver):
    user: User = User.get_user_by_id(booking.user_id)

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
        crossfit_class: CrossFitClass = CrossFitClass.get_every_crossfit_class_by_user_id(booking.class_id)
        sign_in(crossfit_class, webdriver)
        booking.set_as_signed_in()
        send_email(user.mail, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la "
                                                    f"classe di {crossfit_class.name}")
        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.mail, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    users = User.get_every_users()
    threads = []
    for user in users:
        bookings = Booking.get_every_active_booking_by_user_id(user.id)
        if len(bookings) > 0:
            if len(bookings) == 1:
                webdriver = WEBDRIVERFACTORY.get_driver()
                t = Thread(target=booking_sign_in, args=(bookings, webdriver))
                t.start()
                threads.append((t, webdriver))
        else:
            LOGGER.info(f'No active booking found for user {user.name}')

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

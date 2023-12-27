from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import sign_in
from Tasks.Booking import is_still_booked
from Tasks.SendEmail import send_email
from multiprocessing.pool import ThreadPool
from Config import LOGGER
from Workflows import WEBDRIVERFACTORY
from DB.Entities.Booking import Booking
from DB.Entities.User import User
from DB.Entities.CrossFitClass import CrossFitClass
from DB.Entities.BookedClass import BookedClass
import traceback


def error_handler(ex):
    exception = traceback.print_exception(type(ex), ex, ex.__traceback__)
    LOGGER.error(f"An error occurred in booking_sign_in thread.\n{str(ex)}")
    send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", f"Exception: {str(ex)}\nTraceback:\n{str(exception)}")


def booking_sign_in(booked_class: BookedClass, webdriver):
    LOGGER.info(f"Found that I should book {booked_class}")
    user: User = User.get_user_by_id(booked_class.user_id)
    crossfit_class: CrossFitClass = CrossFitClass.get_crossfit_class_by_id(booked_class.class_id)
    booking: Booking = Booking.get_booking_by_user_and_class_id(user.id, crossfit_class.id)

    is_logged_in = login(user, webdriver)

    if is_logged_in:
        try:
            if is_still_booked(crossfit_class, webdriver):
                sign_in(crossfit_class, webdriver)
                message = f"Ciao {user.name}, ti ho fatto il signIn automatico per la classe di {crossfit_class.name}"
                booking.is_signed_in = True
            else:
                message = f"Ciao {user.name}, NON ti ho fatto il signIn automatico per la classe di {crossfit_class.name}"
        except Exception as e:
            message = f"Ciao {user.name}, il tuo signIn automatico per la classe di {crossfit_class.name} è fallito :)\nCausa: {str(e)}\n\n\n\nmannaggia la mad***a :)"
        finally:
            log_out(user, webdriver)
            if booking.is_signed_in:
                booking.set_as_signed_in()
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        message = f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino"
    
    send_email(user.mail, "Auto SignIn", message)

def main():
    webdriver_to_be_closed = []
    users = User.get_every_users()
    with ThreadPool() as pool:
        for user in users:
            bookings = BookedClass.get_booked_class_by_user_id_for_current_datetime(user.id)
            if len(bookings) == 1:
                webdriver = WEBDRIVERFACTORY.get_driver()
                webdriver_to_be_closed.append(webdriver)
                pool.apply_async(booking_sign_in, args=(bookings.pop(), webdriver), error_callback=error_handler)
            else:
                LOGGER.info('No Booked Class Found!')
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

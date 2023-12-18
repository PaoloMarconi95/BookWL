from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import sign_in
from Tasks.Booking import is_still_booked
from Tasks.SendEmail import send_email
import traceback
from multiprocessing.pool import ThreadPool
from Config import CONFIG, LOGGER
from Workflows import WEBDRIVERFACTORY
from DB.Entities.Booking import Booking
from DB.Entities.User import User
from DB.Entities.CrossFitClass import CrossFitClass
from DB.Entities.BookedClass import BookedClass
import traceback


def error_handler(ex):
    exception = traceback.print_exception(type(ex), ex, ex.__traceback__)
    LOGGER.error(f"An error occurred in booking_sign_in thread.\n{str(ex)}\n{exception}")
    send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", f"{str(ex)}\n{exception}")


def booking_sign_in(booked_class: BookedClass, webdriver):
    LOGGER.info(f"Found that I should book {booked_class}")
    user: User = User.get_user_by_id(booked_class.user_id)
    LOGGER.info(f"User correctly retrieved")

    crossfit_class: CrossFitClass = CrossFitClass.get_crossfit_class_by_id(booked_class.class_id)
    LOGGER.info(f"CrossFitClass correctly retrieved")

    booking: Booking = Booking.get_booking_by_user_and_class_id(user.id, crossfit_class.id)
    LOGGER.info(f"Booking correctly retrieved")

    logged_in = login(user, webdriver)

    if logged_in:
        try:
            if is_still_booked(crossfit_class, webdriver):
                sign_in(crossfit_class, webdriver)
                send_email(user.mail, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la "
                            f"classe di {crossfit_class.name}")
                booking.set_as_signed_in()
            else:
                send_email(user.mail, "Auto SignIn", f"Ciao {user.name}, NON ti ho fatto il signIn automatico per la "
                            f"classe di {crossfit_class.name}")
        except Exception as e:
            send_email(user.mail, "Auto SignIn", f"Ciao {user.name}, il tuo signIn automatico per la "
                        f"classe di {crossfit_class.name} è fallito :)\nCausa: {str(e)}\n\n\n\nmannaggia la mad***a :) ")
        finally:
            log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.mail, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

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

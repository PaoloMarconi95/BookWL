from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_and_program_for_current_time, sign_in
from Tasks.SendEmail import send_email
import traceback
from threading import Thread
from Config import CONFIG, LOGGER
from Workflows import WEBDRIVERFACTORY

def main_thread_work(user, webdriver):
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
        # Retrieve booked class for today
        reserved_class, reserved_program = get_booked_class_and_program_for_current_time(webdriver)
        # reserved_class = "WOD"
        if reserved_class is not None:
            # SignIn
            sign_in(reserved_class, reserved_program, webdriver)
            send_email(user.username, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la "
                                                     f"classe di {reserved_class}")

        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.username, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    threads = []
    for user in CONFIG.users:
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

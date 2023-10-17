from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_and_program_for_current_time, sign_in
import Configuration
from Tasks.SendEmail import send_email
import traceback
from threading import Thread
from WebDriver import get_driver

import Log
config = Configuration.get_instance()
users = config.users
log = Log.logger


def main_thread_work(user, webdriver):
    log.info("Starting sign-in process for user " + str(user.name))
    logged_in = False
    attempts = 0
    while not logged_in and attempts < config.MAX_LOGIN_ATTEMPTS:
        try:
            logged_in = login(user, webdriver)
        except AttributeError as e:
            log.error(f'Login for user {user.name} failed! Trying again...')
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
        log.error(f'Login for user {user.name} failed!')
        send_email(user.username, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    threads = []
    for user in users:
        webdriver = get_driver()
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
        log.error(f"FATAL")
        log.error(main_exception)
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        log.info('Program terminated')

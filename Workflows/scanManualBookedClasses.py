from DB.Entities.User import User
from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_and_program_for_current_datetime, sign_in
from Tasks.SendEmail import send_email
import traceback
from threading import Thread
from Config import CONFIG, LOGGER
from Workflows import WEBDRIVERFACTORY
from DB.Database import Database

db = Database('/home/paolo.marconi/CrossFit.db')

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
        # Retrieve booked class for NOW
        reserved_class, reserved_program = get_booked_class_and_program_for_current_date(webdriver, a, b)
        if reserved_class is not None:
            sign_in(reserved_class, reserved_program, webdriver)
        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.username, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")

def main():
    """ threads = []
    for user in CONFIG.users:
        webdriver = WEBDRIVERFACTORY.get_driver()
        t = Thread(target=main_thread_work, args=(user, webdriver))
        t.start()
        threads.append((t, webdriver))

    for t, wb in threads:
        t.join()
        wb.close() """
    
    webdriver = WEBDRIVERFACTORY.get_driver()
    users_cursor = db.execute_query(User.get_users_query())

    users = []
    for user in users_cursor:
        users.append(User.map_query_to_class(user))

    for user in users:
        main_thread_work(user, webdriver)


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

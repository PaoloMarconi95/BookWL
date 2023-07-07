import time

from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_and_program_for_current_time, sign_in
import Configuration
from Tasks.SendEmail import send_email

import Log
config = Configuration.get_instance()
users = config.users
log = Log.logger

def main():
    for user in users:
        log.info("Starting sign-in process for user " + str(user.name))
        logged_in = login(user)
        if logged_in:
            # Retrieve booked class for today
            reserved_class, reserved_program = get_booked_class_and_program_for_current_time()
            # reserved_class = "WOD"
            if reserved_class is not None:
                # SignIn
                sign_in(reserved_class, reserved_program)
                try:
                    send_email(user.username, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la classe di {reserved_class}")
                except Exception as e:
                    log.error("errore nella send_email")
                    log.error(str(e))
                time.sleep(2)
        else:
            log.error(f"Login proccess failed for user {user.name}")

        log_out(user)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(f"FATAL")
        log.error(e)
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))
    finally:
        log.info('Process completed, ending chromedriver task...')
        config.driver.quit()
        log.info('Program terminated')

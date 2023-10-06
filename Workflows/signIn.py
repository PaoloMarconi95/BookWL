from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_and_program_for_current_time, sign_in
import Configuration
from Tasks.SendEmail import send_email
import traceback

import Log
config = Configuration.get_instance()
users = config.users
log = Log.logger


def main():
    for user in users:
        log.info("Starting sign-in process for user " + str(user.name))
        logged_in = False
        attempts = 0
        while not logged_in and attempts < 5:
            try:
                logged_in = login(user)
            except AttributeError as e:
                send_email(user.username, "Auto SignIn Fallito, riprovo",
                           f"Ciao, il sign-in è fallito, ma ci riprovo (massimo alre {attempts}) volte! "
                           f"se non ricevi altre mail significa che è andato tutto bene!")
            finally:
                attempts += 1
        # Retrieve booked class for today
        reserved_class, reserved_program = get_booked_class_and_program_for_current_time()
        # reserved_class = "WOD"
        if reserved_class is not None:
            # SignIn
            sign_in(reserved_class, reserved_program)
            send_email(user.username, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la classe di {reserved_class}")

        log_out(user)


if __name__ == "__main__":
    try:
        main()
    except Exception as main_exception:
        log.error(f"FATAL")
        log.error(main_exception)
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(main_exception))
    finally:
        log.info('Process completed, ending chromedriver task...')
        config.driver.quit()
        log.info('Program terminated')

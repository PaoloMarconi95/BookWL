import time

from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_for_current_time, sign_in
import Configuration
from Tasks.SendEmail import send_email

import Log
config = Configuration.get_instance()
users = config.users
log = Log.logger

def main():
    for user in users:
        log.info("Starting sign-in  process for user " + str(user.name))
        login(user)
        # Retrieve booked class for today
        reserved_class = get_booked_class_for_current_time()
        #reserved_class = "18:00 WOD"
        if reserved_class is not None:
            # SignIn
            sign_in(reserved_class)
            try:
                #send_email(user.username, "Auto SignIn", f"Ciao {user.name}, ti ho fatto il signIn automatico per la classe di {reserved_class}")
                print("mandata")
            except Exception as e:
                log.error("errore nella send_email")
                log.error(str(e))
            time.sleep(5)

        log_out(user)


if __name__ == "__main__":
    main()

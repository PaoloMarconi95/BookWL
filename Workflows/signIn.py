import time

from Tasks.LogIn import login
from Tasks.ChangeUser import log_out
from Tasks.ClassSignIn import get_booked_class_for_current_time, sign_in
from Tasks import Configuration

import Log
users = Configuration.users
log = Log.logger

def main():
    for user in users:
        log.info("Starting booking process for user " + str(user.name))
        login(user)
        # Retrieve booked class for today
        # reserved_class = get_booked_class_for_current_time()
        # if reserved_class is not None:
        #     # SignIn
        #     sign_in(reserved_class)
        #     time.sleep(5)
        #
        # log_out(user.name)


if __name__ == "__main__":
    main()
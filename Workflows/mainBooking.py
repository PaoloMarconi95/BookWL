from Tasks.LogIn import login
from Tasks.Booking import book_class

import Configuration
import Log
config = Configuration.get_instance()
users = config.users
log = Log.logger

def main():
    for user in users:
        log.info("Starting booking process for user " + str(user.name))
        login(user)
        successful = []
        unsuccessful = []
        for book in user.bookings:
            try:
                success = book_class(book)
                if success:
                    successful.append(book)
            except:
                unsuccessful.append(book)
                log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeeded')




if __name__ == "__main__":
    main()
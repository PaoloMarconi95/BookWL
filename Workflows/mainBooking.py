from Tasks.LogIn import login
from Tasks.BookClassByName import book_class

from Tasks import Configuration
import Log
bookings = Configuration.bookings
log = Log.logger

def main():
    login()
    successful = []
    unsuccessful = []
    for book in bookings:
        try:
            success = book_class(book)
            if success:
                successful.append(book)
        except:
            unsuccessful.append(book)
            log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeeded')




if __name__ == "__main__":
    main()
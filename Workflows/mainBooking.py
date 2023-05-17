from Tasks.LogIn import login
from Tasks.BookClassByName import book_class

from Tasks import Configuration
import Log
bookings = Configuration.bookings
log = Log.logger

def main():
    login()
    for book in bookings:
        book_class(book)




if __name__ == "__main__":
    try:
        main()
    except:
        log.error("Fatal error occurred")
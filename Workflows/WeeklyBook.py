import Tasks.BookClass
from Config.Configuration import User
from Config.FutureBookingConfiguration import ClassToBeBooked
from Model.Bookings import Bookings
from Model.BrowserProvider import BrowserProvider
from Model.CrossFitClass import CrossFitClass
from Tasks.SendEmail import send_email
from Config import LOGGER, CONFIG, FUTUREBOOKINGCONFIG
import traceback


def extract_class_array_summary(class_array):
    text = "".join([f"{cfls.class_name} on {cfls.class_date}, " for cfls in class_array])
    return text[:len(text) - 2] + "\n\n"


def generate_email_summary(successful, waitlist, unsuccessful, not_found):
    text = ""
    if len(successful) > 0:
        text += f"Succesfully booked {len(successful)} classes: \n"
        text += extract_class_array_summary(successful)
    if len(waitlist) > 0:
        text += f"Waitlisted {len(waitlist)} classes: \n"
        text += extract_class_array_summary(waitlist)
    if len(unsuccessful) > 0:
        text += f"Could not book {len(unsuccessful)} classes: \n"
        text += extract_class_array_summary(unsuccessful)
    if len(not_found) > 0:
        text += f"Didn't found {len(not_found)} classes: \n"
        text += extract_class_array_summary(not_found)
    return text


def get_booking_result_report(bookings: Bookings, user_bookings: list[ClassToBeBooked]) -> tuple[
    list[str], list[str], list[str], list[str]]:
    successful, unsuccessful, waitlist, not_found, = [], [], [], []
    for book in user_bookings:
        matching_books = list(filter(lambda x: x.name == book.name, bookings.crossfit_classes[book.date]))
        if len(matching_books) == 0:
            not_found.append(book.name)
        else:
            matching_book: CrossFitClass = matching_books[0]
            if matching_book.is_booked:
                successful.append(book.name)
            if matching_book.is_waitlisted:
                waitlist.append(book.name)
            else:
                if not matching_book.is_booked:
                    unsuccessful.append(book.name)

    return successful, unsuccessful, waitlist, not_found


def book_future_bookings(user: User, bp: BrowserProvider):
    LOGGER.info("Starting booking process for user " + str(user.name))
    bookings = Bookings(bp)
    bookings.compute_bookings()
    user_bookings = list(filter(lambda x: x.user_id == user.id, FUTUREBOOKINGCONFIG.classes))
    for user_booking in user_bookings:
        if user_booking.date.date() in bookings.class_rows.keys():
            Tasks.BookClass.book_class(user_booking, bookings.class_rows)

    bookings.compute_bookings()
    successful, unsuccessful, waitlist, not_found = get_booking_result_report(bookings, user_bookings)
    summary = generate_email_summary(successful, waitlist, unsuccessful, not_found)
    send_email(user.mail, "Auto Booking", summary)


def main():
    for usr in CONFIG.users:
        browser_provider = BrowserProvider(usr)
        book_future_bookings(usr, browser_provider)
        browser_provider.dispose()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))

import Tasks.BookClass
from Config.Configuration import User
from Config.FutureBookingConfiguration import ClassToBeBooked
from Model.BookingResult import BookingResult
from Model.Bookings import Bookings
from Model.BrowserProvider import BrowserProvider
from Model.CrossFitClass import CrossFitClass
from Tasks.SendEmail import send_email
from Config import LOGGER, CONFIG, FUTUREBOOKINGCONFIG
import traceback


def extract_class_array_summary(class_array: list[BookingResult]) -> str:
    text = "".join([f"{cfls.name} on {cfls.date.date()} \n" for cfls in class_array])
    return text[:len(text) - 2] + "\n\n"


def get_classes_with_booking_result(classes_to_be_booked: list[ClassToBeBooked], booking_result: BookingResult) -> list[BookingResult]:
    return list(filter(lambda x: x.booking_result == booking_result, classes_to_be_booked))


def generate_email_summary(classes_to_be_booked: list[ClassToBeBooked]) -> str:
    text = ""

    successful = get_classes_with_booking_result(classes_to_be_booked, BookingResult.SUCCESS)
    if len(successful) > 0:
        text += f"Succesfully booked {len(successful)} classes: \n"
        text += extract_class_array_summary(successful)

    waitlist = get_classes_with_booking_result(classes_to_be_booked, BookingResult.WAITLIST)
    if len(waitlist) > 0:
        text += f"Waitlisted {len(waitlist)} classes: \n"
        text += extract_class_array_summary(waitlist)

    unsuccessful = get_classes_with_booking_result(classes_to_be_booked, BookingResult.FAIL)
    if len(unsuccessful) > 0:
        text += f"Could not book {len(unsuccessful)} classes: \n"
        text += extract_class_array_summary(unsuccessful)

    not_found = get_classes_with_booking_result(classes_to_be_booked, BookingResult.NOT_FOUND)
    if len(not_found) > 0:
        text += f"Didn't found {len(not_found)} classes: \n"
        text += extract_class_array_summary(not_found)

    already_booked = get_classes_with_booking_result(classes_to_be_booked, BookingResult.ALREADY_BOOKED)
    if len(already_booked) > 0:
        text += f"Found that {len(already_booked)} classes was already booked: \n"
        text += extract_class_array_summary(already_booked)
    return text


def set_booking_result(bookings: Bookings, classes_to_be_booked: list[ClassToBeBooked]) -> None:
    classes_to_be_booked = [book for book in classes_to_be_booked if book.date.date() in bookings.crossfit_classes.keys()]
    for class_to_be_booked in classes_to_be_booked:
        matching_books = list(filter(lambda x: x.name == class_to_be_booked.name, bookings.crossfit_classes[class_to_be_booked.date.date()]))
        if len(matching_books) == 0:
            class_to_be_booked.booking_result = BookingResult.NOT_FOUND
        else:
            matching_book: CrossFitClass = matching_books[0]
            if matching_book.is_booked:
                class_to_be_booked.booking_result = BookingResult.SUCCESS
            if matching_book.is_waitlisted:
                class_to_be_booked.booking_result = BookingResult.WAITLIST
            else:
                if not matching_book.is_booked:
                    class_to_be_booked.booking_result = BookingResult.FAIL


def book_future_bookings(user: User, bp: BrowserProvider):
    LOGGER.info("Starting booking process for user " + str(user.name))
    bookings = Bookings(bp)
    bookings.compute_bookings()
    classes_to_be_booked = list(filter(lambda x: x.user_id == user.id, FUTUREBOOKINGCONFIG.classes))
    for class_to_be_booked in classes_to_be_booked:
        if class_to_be_booked.date.date() in bookings.class_rows.keys():
            Tasks.BookClass.book_class(class_to_be_booked, bookings.class_rows)

    bookings.compute_bookings()
    set_booking_result(bookings, classes_to_be_booked)
    summary = generate_email_summary(classes_to_be_booked)
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

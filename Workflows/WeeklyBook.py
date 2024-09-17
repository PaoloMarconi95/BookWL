from datetime import datetime, timedelta, date
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
    text = "".join([f"{cfls.name} on {cfls.date} \n" for cfls in class_array])
    return text[:len(text) - 2] + "\n\n"


def get_classes_by_booking_result(classes_to_be_booked: list[ClassToBeBooked], booking_result: BookingResult) -> list[BookingResult]:
    return list(filter(lambda x: x.booking_result == booking_result, classes_to_be_booked))


def get_text_for_booking_result(classes_to_be_booked: list[ClassToBeBooked], booking_result: BookingResult, text: str) -> str:
    final_text = ""
    matching_classes = get_classes_by_booking_result(classes_to_be_booked, booking_result)
    if len(matching_classes) > 0:
        final_text += f"{text} {len(matching_classes)} classes: \n"
        final_text += extract_class_array_summary(matching_classes)
    return final_text


def generate_email_summary(classes_to_be_booked: list[ClassToBeBooked]) -> str:
    text = ""
    text += get_text_for_booking_result(classes_to_be_booked, BookingResult.SUCCESS, "Succesfully booked")
    text += get_text_for_booking_result(classes_to_be_booked, BookingResult.WAITLIST, "Waitlisted")
    text += get_text_for_booking_result(classes_to_be_booked, BookingResult.FAIL, "Could not book")
    text += get_text_for_booking_result(classes_to_be_booked, BookingResult.NOT_FOUND, "Didn't found")
    return text


def remove_punctuation(string: str) -> str:
    replaced_string = string.replace(":", "").replace(".", "")
    return replaced_string


def set_booking_result(bookings: Bookings, classes_to_be_booked: list[ClassToBeBooked]) -> None:
    for class_to_be_booked in classes_to_be_booked:
        matching_books = list(filter(lambda x: remove_punctuation(x.name) in remove_punctuation(class_to_be_booked.name), bookings.crossfit_classes[class_to_be_booked.date]))
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


def get_next_monday_date() -> date:
    today = datetime.now()
    days_ahead = (7 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_monday = today + timedelta(days=days_ahead)
    return next_monday.date()


def get_classes_to_be_booked_for_user(user: User) -> list[ClassToBeBooked]:
    return list(filter(lambda x: x.user_id == user.id, FUTUREBOOKINGCONFIG.classes))


def book_future_bookings(user: User, bp: BrowserProvider):
    LOGGER.info("Starting booking process for user " + str(user.name))
    next_monday = get_next_monday_date()
    bookings = Bookings(bp)
    bookings.compute_bookings_from_date(next_monday)
    classes_to_be_booked = get_classes_to_be_booked_for_user(user)
    for class_to_be_booked in classes_to_be_booked:
        class_to_be_booked.date = next_monday + timedelta(days=class_to_be_booked.week_day)
        Tasks.BookClass.book_class(class_to_be_booked, bookings.class_rows)

    bookings.compute_bookings_from_date(next_monday)
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

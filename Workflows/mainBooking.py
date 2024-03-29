from Tasks.Booking import book_class
from Tasks.SendEmail import send_email
from Enum.BookingResult import BookingResult
from Config import LOGGER
import traceback
from Workflows import WEBDRIVERFACTORY
from DB.Entities.FutureBooking import FutureBooking
from DB.Entities.CrossFitClass import CrossFitClass
from DB.Entities.Booking import Booking
from DB.Entities.User import User
from multiprocessing.pool import ThreadPool


def extract_class_array_summary(class_array):
    text = "".join([f"{cfls.class_name} on {cfls.class_date}, " for cfls in class_array])
    return text[:len(text)-2] + "\n\n"


def generate_email_summary(successful, waitlist, unsuccessful, not_found, already_booked):
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
    if len(already_booked) > 0:
        text += f"Found that you already booked {len(already_booked)} classes: \n"
        text += extract_class_array_summary(already_booked)
    return text


def book_future_bookings(future_bookings, user: User, webdriver):
    LOGGER.info("Starting booking process for user " + str(user.name))
    user.login(webdriver)

    if user.is_logged_in:
        successful = []
        unsuccessful = []
        waitlist = []
        not_found = []
        already_booked = []
        for book in future_bookings:
            try:
                book: FutureBooking = book
                booking_result = book_class(book, webdriver)
                if booking_result == BookingResult.SUCCESS:
                    successful.append(book)
                    # Upsert CorssfitClass
                    crossfit_class = CrossFitClass(name=book.class_name, date=book.class_date, time=book.class_time, program=book.class_program)
                    crossfit_class_id = crossfit_class.upsert()
                    # Upsert Booking
                    booking = Booking(user_id=user.id, class_id=crossfit_class_id, is_signed_in=False)
                    booking.upsert()                        
                elif booking_result == BookingResult.WAITLIST:
                    waitlist.append(book)
                elif booking_result == BookingResult.FAIL:
                    unsuccessful.append(book)
                elif booking_result == BookingResult.NOT_FOUND:
                    not_found.append(book)
                elif booking_result == BookingResult.ALREADY_BOOKED:
                    already_booked.append(book)
            except Exception as innerException:
                unsuccessful.append(book)
                LOGGER.error(f'Book {str(book.class_name)} for date {str(book.class_date)} did not succeed: {str(innerException)}')

        summary = generate_email_summary(successful, waitlist, unsuccessful, not_found, already_booked)
        send_email(user.mail, "Auto Booking", summary)
        user.log_out(webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.mail, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")
        
    return


def main():
    webdriver_to_be_closed = []
    users = User.get_every_users()
    #users = [User(id=0, name='Paolo', mail='paolomarconi1995@gmail.com', password='Internet0Cross')] # Debug
    with ThreadPool() as pool:
        for user in users:
            future_bookings = FutureBooking.get_future_booking_by_user_id(user.id)
            webdriver = WEBDRIVERFACTORY.get_driver()
            webdriver_to_be_closed.append(webdriver)
            pool.apply_async(book_future_bookings, args=(future_bookings, user, webdriver))
        pool.close()
        pool.join()
    
    for wb in webdriver_to_be_closed:
        wb.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))

from ChangeUser import log_out
from Tasks.LogIn import login
from Tasks.Booking import book_class
from Tasks.SendEmail import send_email
from Enum.BookingResult import BookingResult
from Config import CONFIG, LOGGER
import traceback
from threading import Thread
from Workflows import WEBDRIVERFACTORY


def extract_class_array_summary(class_array):
    text = "".join([f"{cls.class_name} on {cls.date}, " for cls in class_array])
    return text[:len(text)-2] + "\n\n"


def generate_email_summary(success, waitlist, unsuccessful, not_found, already_booked):
    text = ""
    if len(success) > 0:
        text += f"Succesfully booked {len(success)} classes: \n"
        text += extract_class_array_summary(success)
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


def main_thread_work(user, webdriver):
    LOGGER.info("Starting booking process for user " + str(user.name))
    logged_in = False
    attempts = 0
    while not logged_in and attempts < CONFIG.max_login_attempts:
        try:
            logged_in = login(user, webdriver)
        except AttributeError as e:
            LOGGER.error(f'Login for user {user.name} failed ({e}). Trying again...')
        finally:
            attempts += 1

    if logged_in:
        successful = []
        unsuccessful = []
        waitlist = []
        not_found = []
        already_booked = []
        for book in user.bookings:
            try:
                success = book_class(book, webdriver)
                if success == BookingResult.SUCCESS:
                    successful.append(book)
                elif success == BookingResult.WAITLIST:
                    waitlist.append(book)
                elif success == BookingResult.FAIL:
                    unsuccessful.append(book)
                elif success == BookingResult.NOT_FOUND:
                    not_found.append(book)
                elif success == BookingResult.ALREADY_BOOKED:
                    already_booked.append(book)
            except Exception as innerException:
                unsuccessful.append(book)
                LOGGER.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeed: {str(innerException)}')

        summary = generate_email_summary(successful, waitlist, unsuccessful, not_found, already_booked)
        send_email(user.name, "Auto Booking", summary)
        log_out(user, webdriver)
    else:
        LOGGER.error(f'Login for user {user.name} failed!')
        send_email(user.name, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")


def main():
    threads = []
    for user in CONFIG.users:
        webdriver = WEBDRIVERFACTORY.get_driver()
        t = Thread(target=main_thread_work, args=(user, webdriver))
        t.start()
        threads.append((t, webdriver))

    for t, wb in threads:
        t.join()
        wb.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))

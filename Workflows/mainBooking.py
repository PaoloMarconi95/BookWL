from ChangeUser import log_out
from Tasks.LogIn import login
from Tasks.Booking import book_class
from Tasks.SendEmail import send_email
from Enum.BookingResult import BookingResult
import Configuration
import Log
import traceback
from WebDriver import get_driver
from threading import Thread

config = Configuration.get_instance()
users = config.users
log = Log.logger

def extract_class_array_summary(class_array):
    text = "".join([f"{cls.class_name} on {cls.date}, " for cls in class_array])
    return text[:len(text)-2] + "\n\n"

def generate_email_summary(success, waitlist, unsuccessful):
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
    return text


def main_thread_work(user, webdriver):
    log.info("Starting booking process for user " + str(user.name))
    logged_in = False
    attempts = 0
    while not logged_in and attempts < config.MAX_LOGIN_ATTEMPTS:
        try:
            logged_in = login(user, webdriver)
        except AttributeError as e:
            log.error(f'Login for user {user.name} failed ({e}). Trying again...')
        finally:
            attempts += 1

    if logged_in:
        successful = []
        unsuccessful = []
        waitlist = []
        for book in user.bookings:
            try:
                success = book_class(book, webdriver)
                if success == BookingResult.SUCCESS:
                    successful.append(book)
                elif success == BookingResult.WAITLIST:
                    waitlist.append(book)
                else:
                    unsuccessful.append(book)
            except Exception as innerException:
                unsuccessful.append(book)
                log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeed: {str(innerException)}')

        summary = generate_email_summary(successful, waitlist, unsuccessful)
        send_email(user.username, "Auto Booking", summary)
        log_out(user, webdriver)
    else:
        log.error(f'Login for user {user.name} failed!')
        send_email(user.username, "Login Fallito!",
                   f"Ciao {user.name}, il tuo login è fallito. Contatta il paolino")



def main():
    threads = []
    for user in users:
        webdriver = get_driver()
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
    finally:
        config.driver.quit()
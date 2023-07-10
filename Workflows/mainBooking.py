from ChangeUser import log_out
from Tasks.LogIn import login
from Tasks.Booking import book_class
from Tasks.SendEmail import send_email
from Enum.BookingResult import BookingResult

import Configuration
import Log

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



def main():
    for user in users:
        log.info("Starting booking process for user " + str(user.name))
        login(user)
        successful = []
        unsuccessful = []
        waitlist = []
        for book in user.bookings:
            try:
                success = book_class(book)
                if success == BookingResult.SUCCESS:
                    successful.append(book)
                elif success == BookingResult.WAITLIST:
                    waitlist.append(book)
                else:
                    unsuccessful.append(book)
            except Exception as innerException:
                unsuccessful.append(book)
                log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeeded: {str(innerException)}')

        summary = generate_email_summary(successful, waitlist, unsuccessful)
        send_email(user.username, "Auto Booking", summary)
        log_out(user)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))
    finally:
        config.driver.quit()
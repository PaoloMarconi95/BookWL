from ChangeUser import log_out
from Tasks.LogIn import login
from Tasks.Booking import book_class
from Tasks.SendEmail import send_email

import Configuration
import Log

config = Configuration.get_instance()
users = config.users
log = Log.logger

def extract_array_summary(array):
    text = "".join([f"{cl.class_name} on {cl.date}, " for cl in array])
    return text[:len(text)-2] + "\n\n"

def generate_email_summary(success, already_booked, unsuccessful):
    text = ""
    if len(success) > 0:
        text += f"Succesfully booked {len(success)} classes: \n"
        text += extract_array_summary(success)
    if len(already_booked) > 0:
        text += f"Found that {len(already_booked)} classes were already booked: \n"
        text += extract_array_summary(already_booked)
    if len(unsuccessful) > 0:
        text += f"Could not book {len(unsuccessful)} classes: \n"
        text += extract_array_summary(unsuccessful)
    return text



def main():
    for user in users:
        log.info("Starting booking process for user " + str(user.name))
        login(user)
        successful = []
        already_booked = []
        unsuccessful = []
        for book in user.bookings:
            try:
                success = book_class(book)
                if success:
                    successful.append(book)
                else:
                    already_booked.append(book)
            except Exception as innerException:
                unsuccessful.append(book)
                log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeeded: {str(innerException)}')

        send_email(user.username, "Auto Booking", generate_email_summary(successful, already_booked, unsuccessful))
        log_out(user)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))
    finally:
        config.driver.quit()
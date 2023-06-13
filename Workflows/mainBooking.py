from ChangeUser import log_out
from Tasks.LogIn import login
from Tasks.Booking import book_class
from Tasks.SendEmail import send_email

import Configuration
import Log

config = Configuration.get_instance()
users = config.users
log = Log.logger

def generate_email_summary(success, already_booked, unsuccess):
    text = ""
    if len(success) > 0:
        text += f"Succesfully booked {len(success)} classes: "
        text += "".join([f"{cl.class_name} for {cl.date}, " for cl in success])
        text = text[:len(text)-2] + "\n"
    if len(already_booked) > 0:
        text += f"Found that {len(already_booked)} classes were already booked: "
        text += "".join([f"{cl.class_name} for {cl.date}, " for cl in already_booked])
        text = text[:len(text)-2] + "\n"
    if len(unsuccess) > 0:
        text += f"Could not book {len(unsuccess)} classes: "
        text += "".join([f"{cl.class_name} for {cl.date}, " for cl in unsuccess])
        text = text[:len(text)-2] + "\n"
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
            except:
                unsuccessful.append(book)
                log.error(f'Book {str(book.class_name)} for date {str(book.date)} did not succeeded')

        send_email(user.username, "Auto Booking", generate_email_summary(successful, already_booked, unsuccessful))
        log_out(user)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        send_email("paolomarconi1995@gmail.com", "Auto SignIn Error", str(e))
    finally:
        config.driver.quit()
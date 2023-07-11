import smtplib
import ssl
import Log
import Configuration
from email.message import EmailMessage

log = Log.logger
config = Configuration.get_instance()

host = "smtp.gmail.com"
port = 465
from_address = "smartbotfit@gmail.com"
password = config.gmail_key


def send_email(dest, subject, body):
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = dest
    msg.set_content(body)
    log.info("email variables initialized")

    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            log.info("logging into SMTP server")
            server.login(from_address, password)
            log.info("sending the email")
            server.send_message(msg)
        log.info("Email correctly sent")
    except Exception as e:
        log.error("Something went wrong sending the email")
        log.error(str(e))

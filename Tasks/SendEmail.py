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
    log.info(f"sending email: {subject}")

    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(from_address, password)
            server.send_message(msg)
    except Exception as e:
        log.error("Something went wrong sending the email")
        log.error(str(e))

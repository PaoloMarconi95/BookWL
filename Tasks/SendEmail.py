import smtplib
import ssl
from Config import CONFIG, LOGGER
from email.message import EmailMessage

host = "smtp.gmail.com"
port = 465
from_address = "smartbotfit@gmail.com"
password = CONFIG.gmail_key


def send_email(dest, subject, body):
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = dest
    msg.set_content(body)
    LOGGER.info(f"sending email: {subject}")

    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(from_address, password)
            server.send_message(msg)
    except Exception as e:
        LOGGER.error("Something went wrong sending the email")
        LOGGER.error(str(e))

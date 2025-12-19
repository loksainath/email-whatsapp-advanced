# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from config import EMAIL_ID, EMAIL_APP_PASSWORD


# def send_email_reply(to_email, subject, body):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = EMAIL_ID
#         msg["To"] = to_email
#         msg["Subject"] = f"Re: {subject}" if subject else "Re:"

#         msg.attach(MIMEText(body, "plain"))

#         # Gmail SMTP
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(EMAIL_ID, EMAIL_APP_PASSWORD)
#             server.send_message(msg)

#         print("✅ Email reply sent successfully")

#     except Exception as e:
#         print(f"⚠ Failed to send email reply: {e}")
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email_reply(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

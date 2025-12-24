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
# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")


# def send_email_reply(to_email, subject, body):
#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_USER
#     msg["To"] = to_email

#     if not subject.lower().startswith("re:"):
#         subject = "Re: " + subject

#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain", "utf-8"))

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL_USER, EMAIL_PASS)
#         server.send_message(msg)


import smtplib
from email.message import EmailMessage
from config import EMAIL_ID, EMAIL_APP_PASSWORD, SMTP_SERVER, SMTP_PORT
from message_queue import dequeue

def send_email_reply(
    to_email: str,
    subject: str,
    body: str,
    in_reply_to: str | None = None
) -> bool:
    """
    Sends a reply email via Gmail SMTP.
    Returns True on success, False on failure.
    """

    if not to_email or not body:
        raise ValueError("Missing recipient or body")

    msg = EmailMessage()
    msg["From"] = EMAIL_ID
    msg["To"] = to_email
    msg["Subject"] = f"Re: {subject or ''}"

    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to

    # UTF-8 safe content
    msg.set_content(body, charset="utf-8")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ID, EMAIL_APP_PASSWORD)
            server.send_message(msg)

        print("📧 Gmail reply sent successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to send Gmail reply: {e}")
        return False

# import imaplib
# import email
# from email.header import decode_header
# from config import EMAIL_ID, EMAIL_APP_PASSWORD, IMAP_SERVER
# from email_cleaner import clean_email_body


# def fetch_unread_emails():
#     emails = []

#     try:
#         # 🔐 Connect to Gmail IMAP
#         mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#         mail.login(EMAIL_ID, EMAIL_APP_PASSWORD)
#         mail.select("INBOX")

#         # 🔍 Search unread emails
#         status, messages = mail.search(None, "UNSEEN")
#         if status != "OK":
#             mail.logout()
#             return emails

#         email_ids = messages[0].split()

#         for num in email_ids:
#             status, msg_data = mail.fetch(num, "(RFC822)")
#             if status != "OK":
#                 continue

#             for response in msg_data:
#                 if not isinstance(response, tuple):
#                     continue

#                 msg = email.message_from_bytes(response[1])

#                 # ---------- SUBJECT (SAFE DECODE) ----------
#                 subject = ""
#                 decoded_subject = decode_header(msg.get("Subject", ""))

#                 for part, encoding in decoded_subject:
#                     if isinstance(part, bytes):
#                         try:
#                             subject += part.decode(encoding or "utf-8", errors="ignore")
#                         except Exception:
#                             subject += part.decode("utf-8", errors="ignore")
#                     else:
#                         subject += part

#                 subject = subject.strip()

#                 # ---------- FROM ----------
#                 from_ = msg.get("From", "").strip()

#                 # ---------- BODY ----------
#                 raw_body = ""

#                 if msg.is_multipart():
#                     for part in msg.walk():
#                         content_type = part.get_content_type()
#                         content_disposition = str(part.get("Content-Disposition", ""))

#                         # 🚫 Skip attachments
#                         if "attachment" in content_disposition.lower():
#                             continue

#                         if content_type in ("text/plain", "text/html"):
#                             payload = part.get_payload(decode=True)
#                             if payload:
#                                 raw_body = payload.decode(errors="ignore")
#                                 break
#                 else:
#                     payload = msg.get_payload(decode=True)
#                     if payload:
#                         raw_body = payload.decode(errors="ignore")

#                 # 🧹 CLEAN HTML → TEXT
#                 clean_body = clean_email_body(raw_body)

#                 # 🚫 Skip empty emails
#                 if not clean_body:
#                     continue

#                 emails.append({
#                     "from": from_,
#                     "subject": subject,
#                     "body": clean_body
#                 })

#         mail.logout()

#     except Exception as e:
#         print(f"⚠ Error reading email, skipped: {e}")

#     return emails


# import imaplib
# import email
# from email.header import decode_header
# from config import EMAIL_ID, EMAIL_APP_PASSWORD, IMAP_SERVER
# from email_cleaner import clean_email_body


# def fetch_unread_emails():
#     print("📨 fetch_unread_emails() called")
#     emails = []

#     if not EMAIL_ID or not EMAIL_APP_PASSWORD:
#         print("❌ EMAIL_ID / EMAIL_APP_PASSWORD missing")
#         return emails

#     try:
#         # 🔐 Connect to Gmail IMAP
#         mail = imaplib.IMAP4_SSL(IMAP_SERVER)
#         mail.login(EMAIL_ID, EMAIL_APP_PASSWORD)
#         mail.select("INBOX")

#         # 🔍 Search UNSEEN emails
#         status, messages = mail.search(None, "UNSEEN")
#         print("🔍 IMAP search result:", messages)

#         if status != "OK":
#             mail.logout()
#             return emails

#         email_ids = messages[0].split()

#         for num in email_ids:
#             status, msg_data = mail.fetch(num, "(RFC822)")
#             if status != "OK":
#                 continue

#             msg = email.message_from_bytes(msg_data[0][1])

#             # ---------- SUBJECT ----------
#             subject = ""
#             decoded = decode_header(msg.get("Subject", ""))

#             for part, encoding in decoded:
#                 if isinstance(part, bytes):
#                     subject += part.decode(encoding or "utf-8", errors="ignore")
#                 else:
#                     subject += part

#             subject = subject.strip()

#             # ---------- FROM ----------
#             from_ = msg.get("From", "").strip()

#             # ---------- BODY ----------
#             raw_body = ""

#             if msg.is_multipart():
#                 for part in msg.walk():
#                     content_type = part.get_content_type()
#                     disposition = str(part.get("Content-Disposition", ""))

#                     if "attachment" in disposition.lower():
#                         continue

#                     if content_type in ("text/plain", "text/html"):
#                         payload = part.get_payload(decode=True)
#                         if payload:
#                             raw_body = payload.decode(errors="ignore")
#                             break
#             else:
#                 payload = msg.get_payload(decode=True)
#                 if payload:
#                     raw_body = payload.decode(errors="ignore")

#             clean_body = clean_email_body(raw_body)

#             if not clean_body:
#                 continue

#             emails.append({
#                 "from": from_,
#                 "subject": subject,
#                 "body": clean_body
#             })

#             # ✅ Mark email as SEEN after processing
#             mail.store(num, "+FLAGS", "\\Seen")

#         mail.logout()

#     except Exception as e:
#         print(f"⚠ IMAP ERROR: {e}")

#     return emails

# import imaplib
# import email
# from email.header import decode_header
# from attachment_handler import extract_attachments

# EMAIL = "chakaliloksainath@gmail.com"
# PASSWORD = "bgyydevoqpgrpafu"

# def fetch_unread_emails():
#     mails = []
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(EMAIL, PASSWORD)
#     mail.select("inbox")

#     status, messages = mail.search(None, "UNSEEN")
#     for num in messages[0].split():
#         _, msg = mail.fetch(num, "(RFC822)")
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg_obj = email.message_from_bytes(response[1])
#                 subject, _ = decode_header(msg_obj["Subject"])[0]
#                 subject = subject.decode() if isinstance(subject, bytes) else subject

#                 body = ""
#                 if msg_obj.is_multipart():
#                     for part in msg_obj.walk():
#                         if part.get_content_type() == "text/plain":
#                             body = part.get_payload(decode=True).decode()
#                 else:
#                     body = msg_obj.get_payload(decode=True).decode()

#                 mails.append({
#                     "from": msg_obj["From"],
#                     "subject": subject,
#                     "body": body
#                 })

#     mail.logout()
#     return mails


import imaplib
import email
import uuid
from email.header import decode_header
from attachment_handler import extract_attachments

EMAIL = "chakaliloksainath@gmail.com"
PASSWORD = "bgyydevoqpgrpafu"
IMAP_SERVER = "imap.gmail.com"


def fetch_unread_emails():
    mails = []

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")

    for num in messages[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")

        for response in msg_data:
            if not isinstance(response, tuple):
                continue

            msg_obj = email.message_from_bytes(response[1])

            # -------------------------------
            # Generate Reply ID (CRITICAL)
            # -------------------------------
            reply_id = str(uuid.uuid4())

            # -------------------------------
            # Decode subject
            # -------------------------------
            subject, encoding = decode_header(msg_obj.get("Subject", ""))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            # -------------------------------
            # Extract body (plain text only)
            # -------------------------------
            body = ""
            if msg_obj.is_multipart():
                for part in msg_obj.walk():
                    if (
                        part.get_content_type() == "text/plain"
                        and "attachment" not in str(part.get("Content-Disposition"))
                    ):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg_obj.get_payload(decode=True).decode(errors="ignore")

            # -------------------------------
            # Extract attachments
            # -------------------------------
            attachments = extract_attachments(msg_obj, reply_id)

            # -------------------------------
            # Build email data object
            # -------------------------------
            mail_data = {
                "from": msg_obj.get("From"),
                "subject": subject,
                "body": body,
                "reply_id": reply_id,
                "message_id": msg_obj.get("Message-ID"),
                "imap_id": num.decode(),
                "attachments": attachments
            }

            mails.append(mail_data)

    mail.logout()
    return mails
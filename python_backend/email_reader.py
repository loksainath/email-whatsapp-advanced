import imaplib
import email
from email.header import decode_header
from config import EMAIL_ID, EMAIL_APP_PASSWORD, IMAP_SERVER
from email_cleaner import clean_email_body


def fetch_unread_emails():
    emails = []

    try:
        # 🔐 Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ID, EMAIL_APP_PASSWORD)
        mail.select("INBOX")

        # 🔍 Search unread emails
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return emails

        email_ids = messages[0].split()

        for num in email_ids:
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            for response in msg_data:
                if not isinstance(response, tuple):
                    continue

                msg = email.message_from_bytes(response[1])

                # ---------- SUBJECT (SAFE DECODE) ----------
                subject = ""
                decoded_subject = decode_header(msg.get("Subject", ""))

                for part, encoding in decoded_subject:
                    if isinstance(part, bytes):
                        try:
                            subject += part.decode(encoding or "utf-8", errors="ignore")
                        except Exception:
                            subject += part.decode("utf-8", errors="ignore")
                    else:
                        subject += part

                subject = subject.strip()

                # ---------- FROM ----------
                from_ = msg.get("From", "").strip()

                # ---------- BODY ----------
                raw_body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition", ""))

                        # 🚫 Skip attachments
                        if "attachment" in content_disposition.lower():
                            continue

                        if content_type in ("text/plain", "text/html"):
                            payload = part.get_payload(decode=True)
                            if payload:
                                raw_body = payload.decode(errors="ignore")
                                break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        raw_body = payload.decode(errors="ignore")

                # 🧹 CLEAN HTML → TEXT
                clean_body = clean_email_body(raw_body)

                # 🚫 Skip empty emails
                if not clean_body:
                    continue

                emails.append({
                    "from": from_,
                    "subject": subject,
                    "body": clean_body
                })

        mail.logout()

    except Exception as e:
        print(f"⚠ Error reading email, skipped: {e}")

    return emails

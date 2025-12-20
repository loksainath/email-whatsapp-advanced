# from email_reader import fetch_unread_emails
# from spam_filter import is_spam
# from summarizer import summarize_text
# from translator import translate_text
# from priority_classifier import classify_priority
# from message_formatter import format_whatsapp_message
# from message_queue import enqueue_message
# from logger import log_event
# from config import ENABLE_SUMMARY


# def main():
#     emails = fetch_unread_emails()
#     print(f"\n📧 UNREAD EMAILS FOUND: {len(emails)}")

#     for i, mail in enumerate(emails, start=1):
#         try:
#             body_text = mail.get("body", "")
#             sender = mail.get("from", "")

#             # 🚫 Spam / Marketing check
#             if is_spam(body_text, sender):
#                 print(f"❌ Email {i} marked as SPAM – Skipped")
#                 log_event("email_logs.json", {
#                     "from": sender,
#                     "subject": mail.get("subject"),
#                     "status": "Spam"
#                 })
#                 continue

#             # 🧠 Summary (optional)
#             summary = summarize_text(body_text) if ENABLE_SUMMARY else body_text

#             # 🌐 Translation (safe, non-blocking)
#             translated_text = translate_text(summary)

#             # 🚨 Priority classification
#             priority = classify_priority(
#                 mail.get("subject", ""),
#                 summary
#             )

#             # 📲 WhatsApp message formatting
#             whatsapp_msg = format_whatsapp_message(
#                 email=mail,
#                 summary=translated_text,   # ✅ use translated text
#                 translation=translated_text,
#                 priority=priority
#             )

#             # 📥 Queue message
#             enqueue_message(whatsapp_msg)
#             print(f"📥 Email {i} added to WhatsApp queue")

#             # 📝 Log success
#             log_event("email_logs.json", {
#                 "from": sender,
#                 "subject": mail.get("subject"),
#                 "priority": priority,
#                 "status": "Queued"
#             })

#         except Exception as e:
#             print(f"⚠ Error processing email {i}: {e}")
#             log_event("email_logs.json", {
#                 "from": mail.get("from"),
#                 "subject": mail.get("subject"),
#                 "status": "Failed",
#                 "error": str(e)
#             })


# if __name__ == "__main__":
#     main()
import os
import time
import threading
from flask import Flask

from email_reader import fetch_unread_emails
from spam_filter import is_spam
from summarizer import summarize_text
from translator import translate_text
from priority_classifier import classify_priority
from message_formatter import format_whatsapp_message
from message_queue import enqueue_message
from logger import log_event
from config import ENABLE_SUMMARY, ENABLE_TRANSLATION


# =========================
# Health Check Web Server (RENDER REQUIRED)
# =========================
app = Flask(__name__)

@app.route("/")
def health():
    return "Email → WhatsApp Service Running", 200


def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# =========================
# Main Background Logic
# =========================
def process_emails():
    try:
        emails = fetch_unread_emails()
    except Exception as e:
        print(f"❌ Failed to fetch emails: {e}")
        return

    print(f"\n📧 UNREAD EMAILS FOUND: {len(emails)}")

    for i, mail in enumerate(emails, start=1):
        sender = mail.get("from", "")
        subject = mail.get("subject", "No Subject")
        body_text = mail.get("body", "")

        try:
            # 🚫 Spam check
            if is_spam(body_text, sender):
                print(f"❌ Email {i} marked as SPAM – Skipped")
                log_event("email_logs.json", {
                    "from": sender,
                    "subject": subject,
                    "status": "Spam"
                })
                continue

            # 🧠 Summary (cloud-safe)
            if ENABLE_SUMMARY and body_text:
                try:
                    processed_text = summarize_text(body_text)
                except Exception:
                    processed_text = body_text[:500]
            else:
                processed_text = body_text

            # 🌐 Translation (cloud-safe)
            if ENABLE_TRANSLATION and processed_text:
                try:
                    processed_text = translate_text(processed_text)
                except Exception:
                    pass

            # 🚨 Priority classification
            priority = classify_priority(subject, processed_text)

            # 📲 WhatsApp message formatting
            whatsapp_msg = format_whatsapp_message(
                email_data={
                    "from": sender,
                    "subject": subject,
                    "body": processed_text
                },
                priority=priority
            )

            # 📥 Queue message
            enqueue_message(whatsapp_msg)
            print(f"📥 Email {i} added to WhatsApp queue")

            # 📝 Log success
            log_event("email_logs.json", {
                "from": sender,
                "subject": subject,
                "priority": priority,
                "status": "Queued"
            })

        except Exception as e:
            print(f"⚠ Error processing email {i}: {e}")
            log_event("email_logs.json", {
                "from": sender,
                "subject": subject,
                "status": "Failed",
                "error": str(e)
            })


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    # Start Render-required web server
    threading.Thread(target=start_health_server, daemon=True).start()

    # Background worker loop
    while True:
        process_emails()
        print("⏳ Sleeping for 2 minutes...")
        time.sleep(200)

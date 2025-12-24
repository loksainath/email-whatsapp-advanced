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
# import os
# import time
# import threading
# from flask import Flask

# from email_reader import fetch_unread_emails
# from spam_filter import is_spam
# from summarizer import summarize_text
# from translator import translate_text
# from priority_classifier import classify_priority
# from message_formatter import format_whatsapp_message
# from message_queue import enqueue_message
# from logger import log_event
# from config import ENABLE_SUMMARY, ENABLE_TRANSLATION

# print("🚀 main.py loaded successfully")

# # =========================
# # Flask App (Render required)
# # =========================
# app = Flask(__name__)

# @app.route("/")
# def health():
#     return "Email → WhatsApp Service Running", 200


# # =========================
# # Email Processing
# # =========================
# def process_emails():
#     print("🔁 process_emails() started")

#     emails = fetch_unread_emails()
#     print(f"📧 UNREAD EMAILS FOUND: {len(emails)}")

#     for i, mail in enumerate(emails, start=1):
#         sender = mail.get("from", "")
#         subject = mail.get("subject", "")
#         body = mail.get("body", "")

#         try:
#             if is_spam(body, sender):
#                 print(f"❌ Email {i} marked as SPAM")
#                 continue

#             processed = body

#             if ENABLE_SUMMARY and body:
#                 try:
#                     processed = summarize_text(body)
#                 except:
#                     processed = body[:500]

#             if ENABLE_TRANSLATION and processed:
#                 try:
#                     processed = translate_text(processed)
#                 except:
#                     pass

#             priority = classify_priority(subject, processed)

#             msg = format_whatsapp_message(
#                 email_data={
#                     "from": sender,
#                     "subject": subject,
#                     "body": processed
#                 },
#                 priority=priority
#             )

#             enqueue_message(msg)
#             print(f"📥 Email {i} queued for WhatsApp")

#             log_event("email_logs.json", {
#                 "from": sender,
#                 "subject": subject,
#                 "priority": priority,
#                 "status": "Queued"
#             })

#         except Exception as e:
#             print("⚠ Processing error:", e)




# # =========================
# # Entry Point
# # =========================
# if __name__ == "__main__":

#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)


# from email_reader import fetch_unread_emails
# from spam_filter import is_spam
# from summarizer import summarize_text
# from translator import translate_text
# from priority_classifier import classify_priority
# from message_formatter import format_whatsapp_message
# from message_queue import enqueue_message
# from logger import log_event
# from config import ENABLE_SUMMARY, ENABLE_TRANSLATION

# print("🚀 main.py started (email processing run)")


# def process_emails():
#     print("🔁 process_emails() started")

#     emails = fetch_unread_emails()
#     print(f"📧 UNREAD EMAILS FOUND: {len(emails)}")

#     for i, mail in enumerate(emails, start=1):
#         sender = mail.get("from", "")
#         subject = mail.get("subject", "")
#         body = mail.get("body", "")

#         try:
#             # 🚫 Spam check
#             if is_spam(body, sender):
#                 print(f"❌ Email {i} marked as SPAM")
#                 continue

#             processed = body

#             # 🧠 Summary
#             if ENABLE_SUMMARY and body:
#                 try:
#                     processed = summarize_text(body)
#                 except Exception:
#                     processed = body[:500]

#             # 🌐 Translation
#             if ENABLE_TRANSLATION and processed:
#                 try:
#                     processed = translate_text(processed)
#                 except Exception:
#                     pass

#             # 🚨 Priority
#             priority = classify_priority(subject, processed)

#             # 🏷 Category (DEFAULT)
#             category = "General"

#             # 📲 WhatsApp message
#             msg = format_whatsapp_message(
#                 email_data={
#                     "from": sender,
#                     "subject": subject,
#                     "body": processed
#                 },
#                 priority=priority,
#                 category=category
#             )

#             enqueue_message(msg)
#             print(f"📥 Email {i} queued for WhatsApp")

#             log_event("email_logs.json", {
#                 "from": sender,
#                 "subject": subject,
#                 "priority": priority,
#                 "category": category,
#                 "status": "Queued"
#             })

#         except Exception as e:
#             print(f"⚠ Error processing email {i}: {e}")


# if __name__ == "__main__":
#     process_emails()


# import os
# import time
# import threading
# from flask import Flask

# from email_reader import fetch_unread_emails
# from spam_filter import is_spam
# from summarizer import summarize_text
# from translator import translate_text
# from priority_classifier import classify_priority
# from message_formatter import format_whatsapp_message
# from message_queue import enqueue_message
# from logger import log_event
# from config import ENABLE_SUMMARY, ENABLE_TRANSLATION

# print("🚀 main.py started (Render-safe mode)")

# # =========================
# # Flask App (REQUIRED by Render)
# # =========================
# app = Flask(__name__)

# @app.route("/")
# def health():
#     return "Email → WhatsApp Service Running", 200


# # =========================
# # Email Processing Logic
# # =========================
# def process_emails():
#     print("🔁 process_emails() triggered")

#     try:
#         emails = fetch_unread_emails()
#     except Exception as e:
#         print(f"❌ Failed to fetch emails: {e}")
#         return

#     print(f"📧 UNREAD EMAILS FOUND: {len(emails)}")

#     for i, mail in enumerate(emails, start=1):
#         sender = mail.get("from", "")
#         subject = mail.get("subject", "")
#         body = mail.get("body", "")

#         try:
#             if is_spam(body, sender):
#                 print(f"❌ Email {i} marked as SPAM")
#                 continue

#             processed = body

#             if ENABLE_SUMMARY and body:
#                 try:
#                     processed = summarize_text(body)
#                 except:
#                     processed = body[:500]

#             if ENABLE_TRANSLATION and processed:
#                 try:
#                     processed = translate_text(processed)
#                 except:
#                     pass

#             priority = classify_priority(subject, processed)

#             whatsapp_msg = format_whatsapp_message(
#                 email_data={
#                     "from": sender,
#                     "subject": subject,
#                     "body": processed
#                 },
#                 priority=priority
#             )

#             enqueue_message(whatsapp_msg)
#             print(f"📥 Email {i} queued for WhatsApp")

#             log_event("email_logs.json", {
#                 "from": sender,
#                 "subject": subject,
#                 "priority": priority,
#                 "status": "Queued"
#             })

#         except Exception as e:
#             print(f"⚠ Error processing email {i}: {e}")


# # =========================
# # Scheduler Loop (NEVER EXITS)
# # =========================
# def scheduler_loop():
#     print("⏰ Scheduler started (every 2 minutes)")
#     while True:
#         process_emails()
#         print("⏳ Sleeping for 2 minutes...")
#         time.sleep(120)


# # =========================
# # Entry Point
# # =========================
# if __name__ == "__main__":
#     # Start scheduler in background
#     threading.Thread(target=scheduler_loop, daemon=True).start()

#     # Start Flask server (this keeps Render alive)
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)

# from email_reader import fetch_unread_emails
# from message_queue import enqueue
# from message_formatter import format_whatsapp_message
# from state_manager import log_email
# import time


# def main():
#     print("📧 Checking Gmail...")

#     emails = fetch_unread_emails()

#     if not emails:
#         print("📭 No new emails")
#         return

#     for mail in emails:
#         try:
#             # ---------------------------------
#             # Format WhatsApp message properly
#             # ---------------------------------
#             formatted_msg = format_whatsapp_message(mail)

#             # ---------------------------------
#             # Enqueue structured message (DICT)
#             # ---------------------------------
#             enqueue(formatted_msg)

#             print(f"✅ Queued email → Reply ID: {formatted_msg['reply_id']}")

#         except Exception as e:
#             print("❌ Failed to process email:", e)

#         time.sleep(0.5)  # small safety delay


# if __name__ == "__main__":
#     main()


from email_reader import fetch_unread_emails
from message_queue import enqueue
from message_formatter import format_whatsapp_message
from state_manager import log_email
import time
import os


INTERVAL_SECONDS = int(os.environ.get("CHECK_INTERVAL", 120))


def main():
    print("📧 Checking Gmail...")

    emails = fetch_unread_emails()

    if not emails:
        print("📭 No new emails")
        return

    for mail in emails:
        try:
            formatted_msg = format_whatsapp_message(mail)
            enqueue(formatted_msg)
            print(f"✅ Queued email → Reply ID: {formatted_msg['reply_id']}")
        except Exception as e:
            print("❌ Failed to process email:", e)

        time.sleep(0.5)


if __name__ == "__main__":
    print("🚀 main.py started (Render-safe mode)")

    while True:
        main()
        print(f"⏳ Sleeping for {INTERVAL_SECONDS} seconds")
        time.sleep(INTERVAL_SECONDS)

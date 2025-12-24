# from message_store import store_mapping


# MAX_WHATSAPP_LEN = 4500

# PRIORITY_STYLE = {
#     "HIGH": {
#         "emoji": "🚨🔥",
#         "label": "HIGH PRIORITY"
#     },
#     "MEDIUM": {
#         "emoji": "⚠️",
#         "label": "MEDIUM PRIORITY"
#     },
#     "LOW": {
#         "emoji": "ℹ️",
#         "label": "LOW PRIORITY"
#     }
# }


# def format_whatsapp_message(email, summary, translation, priority):
#     msg_id = store_mapping(email["from"], email["subject"])

#     style = PRIORITY_STYLE.get(priority, PRIORITY_STYLE["LOW"])

#     message = f"""
# {style["emoji"]} *{style["label"]} EMAIL*

# 👤 From:
# {email["from"]}

# 📌 Subject:
# {email["subject"]}

# 📝 Summary:
# {summary}

# 🆔 Reply ID:
# {msg_id}

# ↩ Reply directly to this WhatsApp message
# """.strip()

#     return message[:MAX_WHATSAPP_LEN]


# import uuid


# def format_whatsapp_message(email_data, priority, category="General"):
#     """
#     Formats WhatsApp message with:
#     From, Subject, Priority, Category
#     """

#     reply_id = str(uuid.uuid4())

#     sender = email_data.get("from", "Unknown")
#     subject = email_data.get("subject", "No Subject")
#     body = email_data.get("body", "")

#     message = f"""
# 📧 *New Email Alert*

# 👤 *From:* {sender}
# 📝 *Subject:* {subject}
# 🚨 *Priority:* {priority}
# 🏷 *Category:* {category}

# —————————
# 📩 *Message:*
# {body}
# —————————

# ↩ Reply to respond
# 🆔 Reply ID: {reply_id}
# """.strip()

#     return message


import uuid
import datetime

from config import (
    ENABLE_SUMMARIZATION,
    ENABLE_TRANSLATION,
    ENABLE_PRIORITY_CLASSIFICATION,
    ENABLE_POPUP_ALERTS,
    ENABLE_NOTIFICATION_SOUND,
)

from state_manager import log_email
from summarizer import summarize_text
from translator import translate_text
from priority_classifier import classify_priority
from email_cleaner import clean_email_body
from message_store import save_reply_mapping

# 🔔 Popup & 🔊 Sound helpers (we will create these next)
from notification import show_popup, play_sound

MAX_WHATSAPP_CHARS = 3500


def format_whatsapp_message(email_data: dict) -> dict:
    """
    Prepares WhatsApp message + dashboard entry
    + popup & sound notifications
    """

    reply_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    sender = str(email_data.get("from", "Unknown Sender"))
    subject = str(email_data.get("subject", "No Subject"))
    raw_body = str(email_data.get("body", ""))

    # ---------------------------
    # Clean email body
    # ---------------------------
    clean_body = clean_email_body(raw_body)

    # ---------------------------
    # Priority classification
    # ---------------------------
    priority = "NORMAL"
    if ENABLE_PRIORITY_CLASSIFICATION:
        try:
            priority = classify_priority(subject, clean_body)
        except Exception:
            priority = "NORMAL"

    # ---------------------------
    # Summarization
    # ---------------------------
    processed_body = clean_body
    if ENABLE_SUMMARIZATION:
        try:
            processed_body = summarize_text(clean_body)
        except Exception:
            processed_body = clean_body

    # ---------------------------
    # Translation
    # ---------------------------
    if ENABLE_TRANSLATION:
        try:
            processed_body = translate_text(processed_body)
        except Exception:
            pass

    content = processed_body.strip()

    if len(content) > MAX_WHATSAPP_CHARS:
        content = content[:MAX_WHATSAPP_CHARS] + "\n\n…(truncated)"

    # ---------------------------
    # Save reply mapping (2-way)
    # ---------------------------
    save_reply_mapping(
        reply_id=reply_id,
        email_data=email_data
    )

    # ---------------------------
    # Dashboard logging (fail-safe)
    # ---------------------------
    try:
        log_email({
            "reply_id": reply_id,
            "from": sender,
            "subject": subject,
            "priority": priority,
            "status": "Queued",
            "time": timestamp,
            "message_id": str(email_data.get("message_id", "")),
            "imap_id": str(email_data.get("imap_id", "")),
        })
    except Exception as e:
        print(f"⚠ Dashboard logging skipped: {e}")

    # ---------------------------
    # WhatsApp message format
    # ---------------------------
    text = (
        "📧 *New Email Received*\n\n"
        f"*From:* {sender}\n"
        f"*Subject:* {subject}\n"
        f"*Priority:* {priority}\n\n"
        f"{content}\n\n"
        "──────────────\n"
        f"*Reply ID:* `{reply_id}`\n\n"
        "↩️ *Reply in this format:*\n"
        f"`{reply_id} | your reply here`"
    )

    # ---------------------------
    # 🔔 Popup Notification
    # ---------------------------
    if ENABLE_POPUP_ALERTS:
        try:
            show_popup(
                title="New Email → WhatsApp",
                message=f"{subject}\nFrom: {sender}"
            )
        except Exception:
            pass

    # ---------------------------
    # 🔊 Notification Sound
    # ---------------------------
    if ENABLE_NOTIFICATION_SOUND:
        try:
            play_sound()
        except Exception:
            pass

    return {
        "reply_id": reply_id,
        "text": text,
        "imap_id": email_data.get("imap_id"),
        "message_id": email_data.get("message_id"),
        "priority": priority,
    }

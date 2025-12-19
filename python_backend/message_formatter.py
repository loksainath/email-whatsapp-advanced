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
import uuid
from message_store import store_mapping


def format_whatsapp_message(email_data, priority="NORMAL"):
    """
    email_data = {
        "from": "user@gmail.com",
        "subject": "Meeting Update",
        "body": "Email content"
    }
    """

    reply_id = str(uuid.uuid4())

    from_email = email_data.get("from")
    subject = email_data.get("subject", "No Subject")
    body = email_data.get("body", "")

    # ✅ Store UUID mapping correctly
    store_mapping(reply_id, from_email, subject)

    message = (
        f"📧 *{subject}*\n"
        f"🚨 Priority: {priority}\n\n"
        f"{body}\n\n"
        f"Reply ID:\n{reply_id}"
    )

    return message

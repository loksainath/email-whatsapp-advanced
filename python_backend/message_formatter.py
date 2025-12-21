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


def format_whatsapp_message(email_data, priority, category="General"):
    """
    Formats WhatsApp message with:
    From, Subject, Priority, Category
    """

    reply_id = str(uuid.uuid4())

    sender = email_data.get("from", "Unknown")
    subject = email_data.get("subject", "No Subject")
    body = email_data.get("body", "")

    message = f"""
📧 *New Email Alert*

👤 *From:* {sender}
📝 *Subject:* {subject}
🚨 *Priority:* {priority}
🏷 *Category:* {category}

—————————
📩 *Message:*
{body}
—————————

↩ Reply to respond
🆔 Reply ID: {reply_id}
""".strip()

    return message

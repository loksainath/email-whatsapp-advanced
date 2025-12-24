# from flask import Flask, request, jsonify
# from message_store import get_mapping
# from email_sender import send_email_reply

# app = Flask(__name__)


# @app.route("/reply", methods=["POST"])
# def handle_reply():
#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"status": "invalid request"}), 400

#     text = data.get("reply", "").strip()

#     # Check for Reply ID
#     if not text or "Reply ID:" not in text:
#         return jsonify({"status": "ignored"}), 200

#     # Extract Reply ID
#     msg_id = text.split("Reply ID:")[-1].strip().split()[0]
#     mapping = get_mapping(msg_id)

#     if not mapping:
#         return jsonify({"status": "invalid id"}), 400

#     # Remove Reply ID line from message body
#     clean_body = text.replace(f"Reply ID: {msg_id}", "").strip()

#     # Send reply email
#     send_email_reply(
#         to_email=mapping["from_email"],
#         subject=mapping.get("subject", "Reply from WhatsApp"),
#         body=clean_body
#     )

#     return jsonify({"status": "email reply sent"}), 200


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)

import re
import json
import os

from email_sender import send_email_reply
from state_manager import mark_replied

# =====================================================
# Safe absolute path
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPLY_MAP_FILE = os.path.join(BASE_DIR, "reply_map.json")


def _load_reply_map() -> dict:
    if not os.path.exists(REPLY_MAP_FILE):
        return {}

    try:
        with open(REPLY_MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def handle_reply(text: str) -> bool:
    """
    Handles WhatsApp reply → Gmail reply.
    Expected format:
    <reply_id> | your reply here
    Returns:
    True  → reply processed & email sent
    False → invalid / failed
    """

    if not text:
        return False

    # Strict reply format
    match = re.match(
        r"^\s*([a-f0-9\-]{36})\s*\|\s*(.+)$",
        text.strip(),
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        print("⚠ Invalid reply format")
        return False

    reply_id, reply_text = match.groups()
    reply_text = reply_text.strip()

    if not reply_text:
        print("⚠ Empty reply ignored")
        return False

    reply_map = _load_reply_map()
    data = reply_map.get(reply_id)

    if not data:
        print(f"⚠ Unknown reply ID: {reply_id}")
        return False

    try:
        send_email_reply(
            to_email=data["to"],
            subject="Re: " + data["subject"],
            body=reply_text,
            in_reply_to=data["message_id"],
        )

        mark_replied(reply_id)
        print("✅ Email reply sent successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to send email reply: {e}")
        return False

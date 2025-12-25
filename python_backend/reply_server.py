# from flask import Flask, request, jsonify
# from message_store import get_mapping
# from email_sender import send_email_reply
# from flask_cors import CORS
# import re

# app = Flask(__name__)
# CORS(app)  # Allow local cross-origin requests


# @app.route("/reply", methods=["POST"])
# def handle_reply():
#     data = request.get_json(silent=True)

#     if not data or "reply" not in data:
#         return jsonify({"error": "Invalid request body"}), 400

#     reply_text = data.get("reply", "").strip()

#     # Extract UUID (Reply ID)
#     match = re.search(
#         r"[0-9a-fA-F]{8}-"
#         r"[0-9a-fA-F]{4}-"
#         r"[0-9a-fA-F]{4}-"
#         r"[0-9a-fA-F]{4}-"
#         r"[0-9a-fA-F]{12}",
#         reply_text
#     )

#     if not match:
#         return jsonify({"error": "Reply ID not found"}), 400

#     reply_id = match.group()
#     mapping = get_mapping(reply_id)

#     if not mapping:
#         return jsonify({"error": "Invalid Reply ID"}), 404

#     from_email = mapping.get("from_email")
#     subject = mapping.get("subject", "Reply from WhatsApp")

#     # Remove Reply ID from message
#     clean_reply = reply_text.replace(reply_id, "").strip()

#     try:
#         send_email_reply(
#             to_email=from_email,
#             subject=subject,   # email_sender already adds "Re:"
#             body=clean_reply
#         )
#     except Exception as e:
#         return jsonify({
#             "error": "Failed to send email reply",
#             "details": str(e)
#         }), 500

#     return jsonify({"status": "Email reply sent successfully"}), 200


# @app.route("/")
# def home():
#     return "✅ Reply server running"


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from message_store import get_mapping
# from email_sender import send_email_reply
# import re

# app = Flask(__name__)
# CORS(app)

# UUID_REGEX = (
#     r"[0-9a-fA-F]{8}-"
#     r"[0-9a-fA-F]{4}-"
#     r"[0-9a-fA-F]{4}-"
#     r"[0-9a-fA-F]{4}-"
#     r"[0-9a-fA-F]{12}"
# )


# @app.route("/reply", methods=["POST"])
# def handle_reply():
#     data = request.get_json(silent=True)

#     if not data:
#         return jsonify({"status": "Ignored empty payload"}), 200

#     reply_text = (
#         data.get("reply") or
#         data.get("message") or
#         ""
#     ).strip()

#     # ✅ Ignore empty / sticker / attachment replies
#     if not reply_text:
#         print("⚠ Empty or non-text WhatsApp message received – ignored")
#         return jsonify({"status": "Ignored empty message"}), 200

#     match = re.search(UUID_REGEX, reply_text)

#     if not match:
#         print("⚠ WhatsApp reply received without Reply ID:", reply_text)
#         return jsonify({"status": "Reply received (no Reply ID)"}), 200

#     reply_id = match.group()
#     mapping = get_mapping(reply_id)

#     if not mapping:
#         return jsonify({"error": "Invalid Reply ID"}), 404

#     from_email = mapping.get("from_email")
#     subject = mapping.get("subject", "WhatsApp Reply")

#     clean_reply = reply_text.replace(reply_id, "").strip()
#     if not clean_reply:
#         clean_reply = "Reply sent from WhatsApp."

#     send_email_reply(
#         to_email=from_email,
#         subject=subject,
#         body=clean_reply
#     )

#     print("✅ Email reply sent to:", from_email)
#     return jsonify({"status": "Email reply sent"}), 200


# @app.route("/")
# def home():
#     return "✅ Reply server running"


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)


# from flask import Flask, request, jsonify
# import os
# import sys

# # =====================================================
# # FIX PYTHON PATH (CRITICAL)
# # =====================================================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# if BASE_DIR not in sys.path:
#     sys.path.insert(0, BASE_DIR)

# from config import DASHBOARD_HOST
# from reply_handler import handle_reply

# app = Flask(__name__)

# # =====================================================
# # Reply Endpoint (WhatsApp → Gmail)
# # =====================================================
# @app.route("/reply", methods=["POST"])
# def reply_endpoint():
#     """
#     Receives WhatsApp replies and forwards them to Gmail.
#     Expected JSON:
#     { "reply": "<reply_id> | your reply here" }
#     """

#     data = request.get_json(silent=True) or {}
#     text = (data.get("reply") or "").strip()

#     print("\n🔥 /reply endpoint hit")
#     print("📩 Incoming WhatsApp text:", text)

#     if not text:
#         return jsonify({"status": "no-text"}), 200

#     try:
#         result = handle_reply(text)

#         if result is False:
#             return jsonify({"status": "invalid-reply"}), 200

#         print("📨 Gmail reply sent successfully")
#         return jsonify({"status": "sent"}), 200

#     except Exception as e:
#         print("❌ Reply processing failed:", e)
#         return jsonify({"status": "error"}), 500


# # =====================================================
# # Startup
# # =====================================================
# if __name__ == "__main__":
#     print(f"🚀 Reply Server running on http://{DASHBOARD_HOST}:5000")
#     app.run(host=DASHBOARD_HOST, port=5000, debug=False)



from flask import Flask, request, jsonify

from email_sender import send_email_reply
from message_store import get_original_email
from state_manager import update_status

app = Flask(__name__)


@app.route("/reply", methods=["POST"])
def reply_from_whatsapp():
    print("📥 HIT /reply endpoint")
    print("📥 Payload:", request.json)
    data = request.json or {}

    reply_id = data.get("reply_id")
    message = data.get("message")

    if not reply_id or not message:
        return jsonify({"error": "Invalid payload"}), 400

    # 🔑 Fetch original email using CORRECT function
    email_data = get_original_email(reply_id)

    if not email_data:
        print("❌ Reply ID not found:", reply_id)
        return jsonify({"error": "Reply ID not found"}), 404

    try:
        print("📧 Preparing Gmail reply")
        send_email_reply(
            to_email=email_data["from"],
            original_subject=email_data["subject"],
            original_message_id=email_data["message_id"],
            reply_text=message
        )

        update_status(reply_id, "Replied")

        print(f"📧 Gmail reply sent successfully → Reply ID: {reply_id}")
        return jsonify({"success": True})

    except Exception as e:
        print("❌ Gmail reply failed:", e)
        return jsonify({"error": "Email send failed"}), 500


if __name__ == "__main__":
    print("▶ Starting Reply Server...")
    app.run(port=5000)

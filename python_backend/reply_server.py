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
from flask import Flask, request, jsonify
from flask_cors import CORS
from message_store import get_mapping
from email_sender import send_email_reply
import re

app = Flask(__name__)
CORS(app)

UUID_REGEX = (
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)


@app.route("/reply", methods=["POST"])
def handle_reply():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "Ignored empty payload"}), 200

    reply_text = (
        data.get("reply") or
        data.get("message") or
        ""
    ).strip()

    # ✅ Ignore empty / sticker / attachment replies
    if not reply_text:
        print("⚠ Empty or non-text WhatsApp message received – ignored")
        return jsonify({"status": "Ignored empty message"}), 200

    match = re.search(UUID_REGEX, reply_text)

    if not match:
        print("⚠ WhatsApp reply received without Reply ID:", reply_text)
        return jsonify({"status": "Reply received (no Reply ID)"}), 200

    reply_id = match.group()
    mapping = get_mapping(reply_id)

    if not mapping:
        return jsonify({"error": "Invalid Reply ID"}), 404

    from_email = mapping.get("from_email")
    subject = mapping.get("subject", "WhatsApp Reply")

    clean_reply = reply_text.replace(reply_id, "").strip()
    if not clean_reply:
        clean_reply = "Reply sent from WhatsApp."

    send_email_reply(
        to_email=from_email,
        subject=subject,
        body=clean_reply
    )

    print("✅ Email reply sent to:", from_email)
    return jsonify({"status": "Email reply sent"}), 200


@app.route("/")
def home():
    return "✅ Reply server running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

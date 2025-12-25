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

from flask import Flask, request, jsonify
from email_sender import send_email_reply
from message_store import get_reply_mapping
from state_manager import update_status

app = Flask(__name__)

@app.route("/reply", methods=["POST"])
def reply_from_whatsapp():
    data = request.json

    reply_id = data.get("reply_id")
    message = data.get("message")

    if not reply_id or not message:
        return jsonify({"error": "Invalid payload"}), 400

    # 🔑 Fetch original email details
    email_data = get_reply_mapping(reply_id)

    if not email_data:
        return jsonify({"error": "Reply ID not found"}), 404

    try:
        send_email_reply(
            to_email=email_data["from"],
            original_subject=email_data["subject"],
            original_message_id=email_data["message_id"],
            reply_text=message
        )

        update_status(reply_id, "Replied")

        print(f"📧 Gmail reply sent for Reply ID: {reply_id}")
        return jsonify({"success": True})

    except Exception as e:
        print("❌ Gmail reply failed:", e)
        return jsonify({"error": "Email send failed"}), 500


if __name__ == "__main__":
    print("▶ Starting Reply Server...")
    app.run(port=5000)

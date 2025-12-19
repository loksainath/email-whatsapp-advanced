from flask import Flask, request, jsonify
from message_store import get_mapping
from email_sender import send_email_reply

app = Flask(__name__)


@app.route("/reply", methods=["POST"])
def handle_reply():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "invalid request"}), 400

    text = data.get("reply", "").strip()

    # Check for Reply ID
    if not text or "Reply ID:" not in text:
        return jsonify({"status": "ignored"}), 200

    # Extract Reply ID
    msg_id = text.split("Reply ID:")[-1].strip().split()[0]
    mapping = get_mapping(msg_id)

    if not mapping:
        return jsonify({"status": "invalid id"}), 400

    # Remove Reply ID line from message body
    clean_body = text.replace(f"Reply ID: {msg_id}", "").strip()

    # Send reply email
    send_email_reply(
        to_email=mapping["from_email"],
        subject=mapping.get("subject", "Reply from WhatsApp"),
        body=clean_body
    )

    return jsonify({"status": "email reply sent"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

from flask import Flask, render_template, jsonify, Response
import json
import os
import csv

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

EMAIL_LOG = os.path.join(PROJECT_DIR, "email_logs.json")
QUEUE_FILE = os.path.join(PROJECT_DIR, "message_queue.json")


def load_json_safe(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else default
    except Exception:
        pass
    return default


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analytics")
def analytics():
    emails = load_json_safe(EMAIL_LOG, [])
    queue = load_json_safe(QUEUE_FILE, [])

    priority_count = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    replied = 0

    for e in emails:
        p = e.get("priority", "LOW")
        priority_count[p] = priority_count.get(p, 0) + 1
        if e.get("status") == "Replied":
            replied += 1

    return jsonify({
        "total_emails": len(emails),
        "queued_messages": len(queue),
        "replies": replied,
        "priority": priority_count
    })


@app.route("/api/logs")
def logs():
    emails = load_json_safe(EMAIL_LOG, [])
    return jsonify(emails[-100:])


@app.route("/download/logs")
def download_logs():
    emails = load_json_safe(EMAIL_LOG, [])

    def generate():
        yield "From,Subject,Priority,Status,Time\n"
        for e in emails:
            yield f"{e.get('from','')},{e.get('subject','')},{e.get('priority','')},{e.get('status','')},{e.get('time','')}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=email_logs.csv"}
    )


if __name__ == "__main__":
    app.run(port=7000, debug=False)

import os
import sys
import json
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

# -------------------------------------------------
# Fix import path (so state_manager can be found)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from state_manager import set_socketio

# -------------------------------------------------
# Flask + SocketIO (NO eventlet)
# -------------------------------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

set_socketio(socketio)

STATE_FILE = os.path.join(PROJECT_ROOT, "system_state.json")


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    if not os.path.exists(STATE_FILE):
        return jsonify([])

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    print("📊 Dashboard running on http://127.0.0.1:7000")
    socketio.run(app, host="127.0.0.1", port=7000, debug=False)
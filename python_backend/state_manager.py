# import json
# import os
# from threading import Lock
# from datetime import datetime

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATE_FILE = os.path.join(BASE_DIR, "system_state.json")

# LOCK = Lock()


# def _load_state():
#     if not os.path.exists(STATE_FILE):
#         return []

#     try:
#         with open(STATE_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data if isinstance(data, list) else []
#     except Exception:
#         return []


# def _save_state(state):
#     with open(STATE_FILE, "w", encoding="utf-8") as f:
#         json.dump(state, f, indent=2)


# # =====================================================
# # LOG NEW EMAIL (Already used by message_formatter)
# # =====================================================
# def log_email(entry: dict):
#     with LOCK:
#         state = _load_state()
#         state.append(entry)
#         _save_state(state)


# # =====================================================
# # UPDATE STATUS (🔥 THIS WAS MISSING)
# # =====================================================
# def update_status(reply_id: str, status: str):
#     """
#     Update message status in dashboard/system_state.json
#     """
#     with LOCK:
#         state = _load_state()
#         updated = False

#         for item in state:
#             if item.get("reply_id") == reply_id:
#                 item["status"] = status
#                 item["updated_at"] = datetime.now().isoformat()
#                 updated = True
#                 break

#         if updated:
#             _save_state(state)


import json
import os
from threading import Lock
from datetime import datetime

# Socket.IO reference (set later)
socketio = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "system_state.json")
LOCK = Lock()


def set_socketio(sock):
    global socketio
    socketio = sock


def _load_state():
    if not os.path.exists(STATE_FILE):
        return []
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def log_email(entry: dict):
    with LOCK:
        state = _load_state()
        state.append(entry)
        _save_state(state)

        if socketio:
            socketio.emit("email_update", entry)


def update_status(reply_id: str, status: str):
    with LOCK:
        state = _load_state()

        for item in state:
            if item.get("reply_id") == reply_id:
                item["status"] = status
                item["updated_at"] = datetime.now().isoformat()

                _save_state(state)

                if socketio:
                    socketio.emit("status_update", item)
                return

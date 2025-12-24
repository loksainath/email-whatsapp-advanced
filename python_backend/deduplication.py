import json
import os
from threading import Lock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "processed_emails.json")

lock = Lock()


def _load():
    if not os.path.exists(FILE):
        return set()

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else set()
    except Exception:
        try:
            os.rename(FILE, FILE + ".corrupted")
        except Exception:
            pass
        return set()


def _save(data_set):
    temp_file = FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(sorted(list(data_set)), f, indent=2)
    os.replace(temp_file, FILE)


def is_done(message_id: str) -> bool:
    if not message_id:
        return False
    with lock:
        return message_id in _load()


def mark_done(message_id: str):
    if not message_id:
        return
    with lock:
        data = _load()
        if message_id not in data:
            data.add(message_id)
            _save(data)

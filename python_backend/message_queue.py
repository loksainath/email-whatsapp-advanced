import json
import os

# Always store queue file in project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(BASE_DIR, "message_queue.json")


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []

    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)


def enqueue_message(message):
    queue = load_queue()
    queue.append(message)
    save_queue(queue)

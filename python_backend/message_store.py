# import json
# import uuid
# import os

# # Always store mapping in project directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STORE_FILE = os.path.join(BASE_DIR, "message_map.json")


# def save_mapping(from_email, subject):
#     msg_id = str(uuid.uuid4())

#     # Load existing mappings safely
#     try:
#         with open(STORE_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             if not isinstance(data, dict):
#                 data = {}
#     except (FileNotFoundError, json.JSONDecodeError):
#         data = {}

#     data[msg_id] = {
#         "from_email": from_email,
#         "subject": subject
#     }

#     # Save back
#     with open(STORE_FILE, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)

#     return msg_id


# def get_mapping(msg_id):
#     try:
#         with open(STORE_FILE, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             return data.get(msg_id)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return None
import json
import os

MAPPING_FILE = "mappings.json"


def _load():
    if not os.path.exists(MAPPING_FILE):
        return {}
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def store_mapping(reply_id, from_email, subject):
    data = _load()
    data[reply_id] = {
        "from_email": from_email,
        "subject": subject
    }
    _save(data)


def get_mapping(reply_id):
    data = _load()
    return data.get(reply_id)



def get_mapping(reply_id):
    data = _load()
    return data.get(reply_id)

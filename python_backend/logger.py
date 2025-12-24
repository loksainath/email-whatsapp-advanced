# import json
# import os
# from datetime import datetime


# def log_event(file_name, data):
#     # Always write logs in project directory
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, file_name)

#     # Ensure log file exists
#     if not os.path.exists(file_path):
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump([], f)

#     # Read existing logs safely
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             logs = json.load(f)
#             if not isinstance(logs, list):
#                 logs = []
#     except Exception:
#         logs = []

#     # Create a copy to avoid mutating original data
#     log_entry = dict(data)
#     log_entry["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     logs.append(log_entry)

#     # Write logs back
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(logs, f, indent=2, ensure_ascii=False)


import json
import os
from datetime import datetime
from threading import Lock

LOG_FILE = "email_logs.json"
lock = Lock()


def log_event(data: dict):
    data["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with lock:
        if not os.path.exists(LOG_FILE):
            logs = []
        else:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []

        logs.append(data)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

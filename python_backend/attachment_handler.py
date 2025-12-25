# #after deployed version
# import os

# ATTACH_DIR = "attachments"

# os.makedirs(ATTACH_DIR, exist_ok=True)


# def save_attachment(part):
#     filename = part.get_filename()
#     if not filename:
#         return None

#     path = os.path.join(ATTACH_DIR, filename)
#     with open(path, "wb") as f:
#         f.write(part.get_payload(decode=True))

#     return path


import os
from email.message import Message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")

os.makedirs(ATTACHMENTS_DIR, exist_ok=True)


def extract_attachments(email_msg: Message, reply_id: str):
    """
    Extract attachments from email and save them to python_backend/attachments
    Returns list of file paths
    """
    files = []

    for part in email_msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            if not filename:
                continue

            safe_name = f"{reply_id}_{filename}"
            path = os.path.join(ATTACHMENTS_DIR, safe_name)

            try:
                with open(path, "wb") as f:
                    f.write(part.get_payload(decode=True))
                files.append(path)
            except Exception as e:
                print(f"⚠ Attachment save failed: {e}")

    return files

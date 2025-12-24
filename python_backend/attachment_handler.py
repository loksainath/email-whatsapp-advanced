#after deployed version
import os

ATTACH_DIR = "attachments"

os.makedirs(ATTACH_DIR, exist_ok=True)


def save_attachment(part):
    filename = part.get_filename()
    if not filename:
        return None

    path = os.path.join(ATTACH_DIR, filename)
    with open(path, "wb") as f:
        f.write(part.get_payload(decode=True))

    return path

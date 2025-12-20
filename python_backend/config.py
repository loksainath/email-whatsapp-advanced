# import os
# from dotenv import load_dotenv

# load_dotenv()

# # =========================
# # Gmail Configuration
# # =========================
# EMAIL_ID = os.getenv("EMAIL_ID")
# EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# # =========================
# # IMAP Configuration
# # =========================
# IMAP_SERVER = "imap.gmail.com"

# # =========================
# # WhatsApp Configuration
# # =========================
# WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")

# # =========================
# # Language Configuration
# # =========================
# TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# # =========================
# # Feature Toggles (SAFE)
# # =========================
# ENABLE_SUMMARY = os.getenv("ENABLE_SUMMARY", "false").lower() == "true"
# ENABLE_TRANSLATION = os.getenv("ENABLE_TRANSLATION", "false").lower() == "true"
# ENABLE_ATTACHMENTS = os.getenv("ENABLE_ATTACHMENTS", "false").lower() == "true"
# SEND_EACH_UNREAD = os.getenv("SEND_EACH_UNREAD", "false").lower() == "true"
import os
from dotenv import load_dotenv

# Load environment variables (works locally, safe on Render)
load_dotenv()

# =========================
# Gmail Configuration
# =========================
EMAIL_ID = os.getenv("EMAIL_ID", "")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

# =========================
# IMAP Configuration
# =========================
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

# =========================
# WhatsApp Configuration
# =========================
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "")

# =========================
# Language Configuration
# =========================
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# =========================
# Feature Toggles (CLOUD SAFE)
# =========================
def env_bool(name: str, default: bool = False) -> bool:
    """Safely parse boolean environment variables"""
    return os.getenv(name, str(default)).lower() in ("true", "1", "yes", "on")


ENABLE_SUMMARY = env_bool("ENABLE_SUMMARY", False)
ENABLE_TRANSLATION = env_bool("ENABLE_TRANSLATION", False)
ENABLE_ATTACHMENTS = env_bool("ENABLE_ATTACHMENTS", False)
SEND_EACH_UNREAD = env_bool("SEND_EACH_UNREAD", False)

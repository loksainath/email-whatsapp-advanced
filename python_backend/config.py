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

# Load environment variables (works locally, ignored safely on Render)
load_dotenv()

# =========================
# Gmail Configuration
# =========================
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# =========================
# IMAP Configuration
# =========================
IMAP_SERVER = "imap.gmail.com"

# =========================
# WhatsApp Configuration
# =========================
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")

# =========================
# Language Configuration
# =========================
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# =========================
# Feature Toggles (CLOUD SAFE)
# =========================
ENABLE_SUMMARY = os.getenv("ENABLE_SUMMARY", "false").lower() == "true"
ENABLE_TRANSLATION = os.getenv("ENABLE_TRANSLATION", "false").lower() == "true"
ENABLE_ATTACHMENTS = os.getenv("ENABLE_ATTACHMENTS", "false").lower() == "true"
SEND_EACH_UNREAD = os.getenv("SEND_EACH_UNREAD", "false").lower() == "true"

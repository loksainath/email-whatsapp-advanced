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
# import os
# from dotenv import load_dotenv

# # Load environment variables (works locally, safe on Render)
# load_dotenv()

# # =========================
# # Gmail Configuration
# # =========================
# EMAIL_ID = os.getenv("EMAIL_ID", "")
# EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

# # =========================
# # IMAP Configuration
# # =========================
# IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

# # =========================
# # WhatsApp Configuration
# # =========================
# WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "")

# # =========================
# # Language Configuration
# # =========================
# TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# # =========================
# # Feature Toggles (CLOUD SAFE)
# # =========================
# def env_bool(name: str, default: bool = False) -> bool:
#     """Safely parse boolean environment variables"""
#     return os.getenv(name, str(default)).lower() in ("true", "1", "yes", "on")


# ENABLE_SUMMARY = env_bool("ENABLE_SUMMARY", False)
# ENABLE_TRANSLATION = env_bool("ENABLE_TRANSLATION", False)
# ENABLE_ATTACHMENTS = env_bool("ENABLE_ATTACHMENTS", False)
# SEND_EACH_UNREAD = env_bool("SEND_EACH_UNREAD", False)


# import os
# from dotenv import load_dotenv

# # ==================================================
# # Load environment variables
# # ==================================================
# # Works locally, ignored safely on Render / Railway
# load_dotenv()

# # ==================================================
# # Gmail / Email Configuration
# # ==================================================
# EMAIL_ID = os.getenv("EMAIL_ID", "").strip()
# EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "").strip()

# IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# # ==================================================
# # WhatsApp Configuration
# # ==================================================
# # Must be in international format without + or spaces
# # Example: 919876543210
# WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "").strip()

# WHATSAPP_SERVER_URL = os.getenv(
#     "WHATSAPP_SERVER_URL",
#     "http://127.0.0.1:3000"
# )

# PYTHON_BACKEND_URL = os.getenv(
#     "PYTHON_BACKEND_URL",
#     "http://127.0.0.1:5000"
# )

# # ==================================================
# # Language / AI Configuration
# # ==================================================
# TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")

# # ==================================================
# # Feature Toggles (SAFE FOR CLOUD)
# # ==================================================
# def env_bool(name: str, default: bool = False) -> bool:
#     """
#     Safely parse boolean environment variables.
#     Accepted true values:
#     true, 1, yes, on
#     """
#     return os.getenv(name, str(default)).lower() in ("true", "1", "yes", "on")


# ENABLE_SUMMARY = env_bool("ENABLE_SUMMARY", True)
# ENABLE_TRANSLATION = env_bool("ENABLE_TRANSLATION", False)
# ENABLE_ATTACHMENTS = env_bool("ENABLE_ATTACHMENTS", True)
# ENABLE_SOUND_ALERT = env_bool("ENABLE_SOUND_ALERT", True)

# # ==================================================
# # Email Processing Behavior
# # ==================================================
# # Prevent duplicate WhatsApp messages
# PREVENT_DUPLICATES = env_bool("PREVENT_DUPLICATES", True)

# # Send WhatsApp for every unread mail (not only new)
# SEND_EACH_UNREAD = env_bool("SEND_EACH_UNREAD", False)

# # ==================================================
# # Timing / Scheduler
# # ==================================================
# EMAIL_POLL_INTERVAL = int(os.getenv("EMAIL_POLL_INTERVAL", "120"))  # seconds

# # ==================================================
# # Storage / Files
# # ==================================================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# QUEUE_FILE = os.path.join(BASE_DIR, "message_queue.json")
# PROCESSED_FILE = os.path.join(BASE_DIR, "processed_emails.json")
# REPLY_MAP_FILE = os.path.join(BASE_DIR, "reply_map.json")
# LOG_FILE = os.path.join(BASE_DIR, "email_logs.json")


import os
from dotenv import load_dotenv
from pathlib import Path

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# =====================================================
# EMAIL CONFIGURATION
# =====================================================
EMAIL_ID = os.getenv("EMAIL_ID", "").strip()
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "").strip()

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")

IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# =====================================================
# WHATSAPP CONFIGURATION
# =====================================================
# ⚠️ Must be different from logged-in WhatsApp number
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "").strip()

WHATSAPP_SERVER_URL = os.getenv(
    "WHATSAPP_SERVER_URL",
    "http://127.0.0.1:3000"
)

WHATSAPP_SEND_ENDPOINT = f"{WHATSAPP_SERVER_URL}/send"
WHATSAPP_READY_ENDPOINT = f"{WHATSAPP_SERVER_URL}/ready"

# =====================================================
# SCHEDULER CONFIGURATION
# =====================================================
SCHEDULER_INTERVAL_SECONDS = int(
    os.getenv("SCHEDULER_INTERVAL_SECONDS", 300)
)

MAX_EMAILS_PER_CYCLE = int(
    os.getenv("MAX_EMAILS_PER_CYCLE", 10)
)

# =====================================================
# TRANSLATION CONFIGURATION
# =====================================================
ENABLE_TRANSLATION = os.getenv(
    "ENABLE_TRANSLATION", "false"
).lower() == "true"

TARGET_LANGUAGE = os.getenv(
    "TARGET_LANGUAGE", "en"
).lower()

# =====================================================
# SUMMARIZATION CONFIGURATION
# =====================================================
ENABLE_SUMMARIZATION = os.getenv(
    "ENABLE_SUMMARIZATION", "true"
).lower() == "true"

SUMMARY_MAX_SENTENCES = int(
    os.getenv("SUMMARY_MAX_SENTENCES", 3)
)

# =====================================================
# PRIORITY CLASSIFICATION
# =====================================================
ENABLE_PRIORITY_CLASSIFICATION = os.getenv(
    "ENABLE_PRIORITY_CLASSIFICATION", "true"
).lower() == "true"

# =====================================================
# POPUP & SOUND NOTIFICATIONS (NEW)
# =====================================================
ENABLE_POPUP_ALERTS = os.getenv(
    "ENABLE_POPUP_ALERTS", "true"
).lower() == "true"

ENABLE_NOTIFICATION_SOUND = os.getenv(
    "ENABLE_NOTIFICATION_SOUND", "true"
).lower() == "true"

# Sound file (used by dashboard & python notifier)
NOTIFICATION_SOUND_FILE = os.getenv(
    "NOTIFICATION_SOUND_FILE",
    str(BASE_DIR / "dashboard" / "static" / "sound.mp3")
)

# =====================================================
# WHATSAPP REPLY HANDLING
# =====================================================
ENABLE_WHATSAPP_REPLY = os.getenv(
    "ENABLE_WHATSAPP_REPLY", "true"
).lower() == "true"

# reply | forward | new
EMAIL_REPLY_MODE = os.getenv(
    "EMAIL_REPLY_MODE", "reply"
).lower()

# =====================================================
# DASHBOARD CONFIGURATION
# =====================================================
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "127.0.0.1")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 7000))

# =====================================================
# FILE PATHS (CENTRALIZED)
# =====================================================
LOG_DIR = BASE_DIR / "logs"
ATTACHMENTS_DIR = BASE_DIR / "attachments"

MESSAGE_QUEUE_FILE = BASE_DIR / "message_queue.json"
REPLY_MAP_FILE = BASE_DIR / "reply_map.json"
PROCESSED_EMAILS_FILE = BASE_DIR / "processed_emails.json"
SYSTEM_STATE_FILE = BASE_DIR / "system_state.json"

# Ensure directories exist
LOG_DIR.mkdir(exist_ok=True)
ATTACHMENTS_DIR.mkdir(exist_ok=True)

# =====================================================
# FAIL-FAST VALIDATION
# =====================================================
REQUIRED_VARS = {
    "EMAIL_ID": EMAIL_ID,
    "EMAIL_APP_PASSWORD": EMAIL_APP_PASSWORD,
    "WHATSAPP_NUMBER": WHATSAPP_NUMBER,
}

missing = [k for k, v in REQUIRED_VARS.items() if not v]

if missing:
    raise RuntimeError(
        f"❌ Missing required environment variables: {missing}"
    )

# =====================================================
# DEBUG SUMMARY (OPTIONAL)
# =====================================================
if os.getenv("DEBUG_CONFIG", "false").lower() == "true":
    print("✅ Configuration Loaded Successfully")

import sys
import os

from config import (
    ENABLE_POPUP_ALERTS,
    ENABLE_NOTIFICATION_SOUND,
    NOTIFICATION_SOUND_FILE
)

# -------------------------------
# Try loading plyer notification
# -------------------------------
try:
    from plyer import notification
except Exception:
    notification = None


# -------------------------------
# 🔔 Popup Notification
# -------------------------------
def show_popup(title: str, message: str):
    """
    Cross-platform desktop popup notification
    """
    if not ENABLE_POPUP_ALERTS:
        return

    if not notification:
        return

    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except Exception:
        pass


# -------------------------------
# 🔊 Sound Notification
# -------------------------------
def play_sound():
    """
    Plays notification sound (Windows/Linux/macOS safe)
    """
    if not ENABLE_NOTIFICATION_SOUND:
        return

    try:
        # ▶ Windows (preferred)
        if sys.platform.startswith("win"):
            if os.path.exists(NOTIFICATION_SOUND_FILE):
                import winsound
                winsound.PlaySound(
                    NOTIFICATION_SOUND_FILE,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            else:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)

        # ▶ Linux / macOS fallback
        else:
            print("\a", end="", flush=True)

    except Exception:
        pass

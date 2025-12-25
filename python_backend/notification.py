# import sys
# import os
# from win10toast import ToastNotifier
# import threading
# from config import (
#     ENABLE_POPUP_ALERTS,
#     ENABLE_NOTIFICATION_SOUND,
#     NOTIFICATION_SOUND_FILE
# )

# # -------------------------------
# # Try loading plyer notification
# # -------------------------------
# try:
#     from plyer import notification
# except Exception:
#     notification = None


# # -------------------------------
# # 🔔 Popup Notification
# # -------------------------------
# def show_popup(title: str, message: str):
#     """
#     Cross-platform desktop popup notification
#     """
#     if not ENABLE_POPUP_ALERTS:
#         return

#     if not notification:
#         return

#     try:
#         notification.notify(
#             title=title,
#             message=message,
#             timeout=5
#         )
#     except Exception:
#         pass


# # -------------------------------
# # 🔊 Sound Notification
# # -------------------------------
# def play_sound():
#     """
#     Plays notification sound (Windows/Linux/macOS safe)
#     """
#     if not ENABLE_NOTIFICATION_SOUND:
#         return

#     try:
#         # ▶ Windows (preferred)
#         if sys.platform.startswith("win"):
#             if os.path.exists(NOTIFICATION_SOUND_FILE):
#                 import winsound
#                 winsound.PlaySound(
#                     NOTIFICATION_SOUND_FILE,
#                     winsound.SND_FILENAME | winsound.SND_ASYNC
#                 )
#             else:
#                 import winsound
#                 winsound.MessageBeep(winsound.MB_ICONASTERISK)

#         # ▶ Linux / macOS fallback
#         else:
#             print("\a", end="", flush=True)

#     except Exception:
#         pass


from plyer import notification
import threading
import os

def show_popup(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Email → WhatsApp System",
            timeout=5
        )
    except Exception as e:
        print("⚠ Popup failed:", e)


def play_sound():
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass

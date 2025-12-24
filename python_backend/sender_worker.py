# from message_queue import load_queue, save_queue
# from whatsapp_client import send_whatsapp_message
# from config import WHATSAPP_NUMBER
# import requests
# import time


# def whatsapp_ready():
#     try:
#         r = requests.get("http://localhost:3000/health", timeout=3)
#         if r.status_code != 200:
#             return False
#         return r.json().get("status") == "ready"
#     except Exception:
#         return False


# print("🚀 WhatsApp Sender Worker Started")
# print("⏳ Waiting for WhatsApp readiness...")

# # 🔒 WAIT UNTIL WHATSAPP IS FULLY CONNECTED
# while not whatsapp_ready():
#     time.sleep(5)

# print("✅ WhatsApp is ready for sending")

# while True:
#     try:
#         queue = load_queue()

#         if not queue:
#             time.sleep(10)
#             continue

#         message = queue[0]

#         if not isinstance(message, str) or not message.strip():
#             queue.pop(0)
#             save_queue(queue)
#             continue

#         print("📲 Sending WhatsApp message...")
#         success = send_whatsapp_message(message, WHATSAPP_NUMBER)

#         if success:
#             print("✅ Message sent successfully")
#             queue.pop(0)
#             save_queue(queue)
#             time.sleep(30)  # WhatsApp cooldown
#         else:
#             print("❌ Send failed, retrying in 30s")
#             time.sleep(30)

#     except Exception as e:
#         print(f"⚠ Sender worker error: {e}")
#         time.sleep(10)


# import time
# import requests
# from message_queue import dequeue_message
# from config import WHATSAPP_NUMBER

# WHATSAPP_SERVER_URL = "http://127.0.0.1:3000/send"

# print("🚀 WhatsApp Sender Worker Started")

# while True:
#     msg = dequeue_message()

#     if not msg:
#         time.sleep(5)
#         continue

#     while True:
#         try:
#             response = requests.post(
#                 WHATSAPP_SERVER_URL,
#                 json={
#                     "number": WHATSAPP_NUMBER,
#                     "message": msg
#                 },
#                 timeout=10
#             )

#             if response.status_code == 200:
#                 print("✅ WhatsApp message sent")
#                 break

#             elif response.status_code == 503:
#                 # WhatsApp not ready yet
#                 print("⏳ WhatsApp not ready, retrying in 10s...")
#                 time.sleep(10)

#             else:
#                 print("❌ WhatsApp send failed:", response.text)
#                 break

#         except Exception as e:
#             print("❌ Error sending WhatsApp:", e)
#             time.sleep(10)

#     # 🕒 Rate limit to avoid WhatsApp ban
#     time.sleep(15)


import time
import requests

from config import (
    WHATSAPP_SERVER_URL,
    WHATSAPP_NUMBER,
    ENABLE_POPUP_ALERTS,
    ENABLE_NOTIFICATION_SOUND
)

from message_queue import dequeue, enqueue
from state_manager import update_status
from notification import show_popup, play_sound


SEND_ENDPOINT = f"{WHATSAPP_SERVER_URL}/send"
READY_ENDPOINT = f"{WHATSAPP_SERVER_URL}/ready"

SEND_DELAY_SECONDS = 2
RETRY_DELAY_SECONDS = 5


def is_whatsapp_ready() -> bool:
    """
    Check if WhatsApp Node server is ready
    """
    try:
        r = requests.get(READY_ENDPOINT, timeout=5)
        return r.status_code == 200
    except Exception:
        return False


def start_worker():
    print("🚀 WhatsApp Sender Worker Started")

    # Wait for WhatsApp readiness
    while not is_whatsapp_ready():
        print("⏳ Waiting for WhatsApp connection...")
        time.sleep(3)

    print("✅ WhatsApp is READY")

    while True:
        msg = dequeue()

        # ---------------------------------
        # 🔒 SAFETY GUARDS (CRITICAL FIX)
        # ---------------------------------
        if not msg:
            time.sleep(1)
            continue

        if not isinstance(msg, dict):
            print("⚠ Skipping invalid queued message (not dict)")
            continue

        try:
            payload = {
                "number": WHATSAPP_NUMBER,
                "message": msg["text"]
            }

            r = requests.post(
                SEND_ENDPOINT,
                json=payload,
                timeout=30
            )

            if r.status_code != 200:
                raise RuntimeError("WhatsApp send failed")

            print("📤 Sent to WhatsApp:", msg["reply_id"])

            # Update dashboard status
            update_status(
                reply_id=msg["reply_id"],
                status="Sent"
            )

            # 🔔 Popup
            if ENABLE_POPUP_ALERTS:
                show_popup(
                    title="WhatsApp Sent",
                    message=f"Message delivered\nReply ID: {msg['reply_id']}"
                )

            # 🔊 Sound
            if ENABLE_NOTIFICATION_SOUND:
                play_sound()

            time.sleep(SEND_DELAY_SECONDS)

        except Exception as e:
            print("❌ Send failed, re-queueing:", e)

            # Requeue ONLY valid messages
            if isinstance(msg, dict):
                enqueue(msg)

                update_status(
                    reply_id=msg.get("reply_id"),
                    status="Retrying"
                )

            time.sleep(RETRY_DELAY_SECONDS)


if __name__ == "__main__":
    start_worker()

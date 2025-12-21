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
import time
import requests
from message_queue import dequeue_message
from config import WHATSAPP_NUMBER

WHATSAPP_SERVER_URL = "http://127.0.0.1:3000/send"

print("🚀 WhatsApp Sender Worker Started")

while True:
    msg = dequeue_message()

    if not msg:
        time.sleep(5)
        continue

    while True:
        try:
            response = requests.post(
                WHATSAPP_SERVER_URL,
                json={
                    "number": WHATSAPP_NUMBER,
                    "message": msg
                },
                timeout=10
            )

            if response.status_code == 200:
                print("✅ WhatsApp message sent")
                break

            elif response.status_code == 503:
                # WhatsApp not ready yet
                print("⏳ WhatsApp not ready, retrying in 10s...")
                time.sleep(10)

            else:
                print("❌ WhatsApp send failed:", response.text)
                break

        except Exception as e:
            print("❌ Error sending WhatsApp:", e)
            time.sleep(10)

    # 🕒 Rate limit to avoid WhatsApp ban
    time.sleep(15)

# import requests

# WHATSAPP_API = "http://localhost:3000/send"


# def send_whatsapp_message(message: str, number: str) -> bool:
#     payload = {
#         "number": number,
#         "message": message
#     }

#     try:
#         response = requests.post(
#             WHATSAPP_API,
#             json=payload,
#             timeout=10
#         )
#         response.raise_for_status()
#         return True

#     except Exception as e:
#         print("❌ WhatsApp API error:", e)
#         return False


import requests
import time

WHATSAPP_API = "http://127.0.0.1:3000/send"
HEALTH_API = "http://127.0.0.1:3000/health"

TIMEOUT = 10
MAX_RETRIES = 3


def whatsapp_ready() -> bool:
    """Check if WhatsApp Node server is ready"""
    try:
        r = requests.get(HEALTH_API, timeout=3)
        return r.status_code == 200 and r.json().get("status") == "ready"
    except Exception:
        return False


def send_whatsapp_message(message: str, number: str) -> bool:
    """
    Send message to WhatsApp via Node server
    Returns True if sent successfully
    """

    if not message or not number:
        print("❌ Invalid WhatsApp payload")
        return False

    # 🔄 Wait until WhatsApp is ready
    for _ in range(5):
        if whatsapp_ready():
            break
        print("⏳ Waiting for WhatsApp readiness...")
        time.sleep(3)
    else:
        print("❌ WhatsApp not ready")
        return False

    payload = {
        "number": number,
        "message": message
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                WHATSAPP_API,
                json=payload,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                print("✅ WhatsApp message sent")
                return True

            elif response.status_code == 503:
                print("⏳ WhatsApp busy, retrying...")
                time.sleep(4)

            else:
                print("❌ WhatsApp API error:", response.text)
                return False

        except Exception as e:
            print(f"❌ WhatsApp send error (attempt {attempt}):", e)
            time.sleep(4)

    print("❌ Failed to send WhatsApp message after retries")
    return False
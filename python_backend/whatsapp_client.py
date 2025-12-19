import requests

WHATSAPP_API = "http://localhost:3000/send"


def send_whatsapp_message(message: str, number: str) -> bool:
    payload = {
        "number": number,
        "message": message
    }

    try:
        response = requests.post(
            WHATSAPP_API,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return True

    except Exception as e:
        print("❌ WhatsApp API error:", e)
        return False

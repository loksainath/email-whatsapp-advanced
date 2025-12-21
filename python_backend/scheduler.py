import time
from main import process_emails

INTERVAL_SECONDS = 300  # 5 minutes

print("⏰ Scheduler started (checks every 5 minutes)")

while True:
    try:
        process_emails()
    except Exception as e:
        print(f"⚠ Scheduler error: {e}")

    time.sleep(INTERVAL_SECONDS)

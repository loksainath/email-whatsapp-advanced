# import time
# import subprocess
# import sys
# import os

# print("⏰ Scheduler started (checks every 1 minutes)")

# # Absolute path to main.py
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MAIN_FILE = os.path.join(BASE_DIR, "main.py")

# while True:
#     try:
#         # Use same Python interpreter that runs scheduler
#         subprocess.run([sys.executable, MAIN_FILE], check=True)
#     except Exception as e:
#         print(f"⚠ Scheduler error: {e}")

#     # Sleep for 1 minutes
#     time.sleep(100)
import time
import subprocess
import sys
import os
from config import SCHEDULER_INTERVAL_SECONDS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_main():
    try:
        print("🚀 Running main.py...")
        subprocess.run(
            [sys.executable, "main.py"],
            cwd=BASE_DIR,
            check=False
        )
    except Exception as e:
        print("❌ Failed to run main.py:", e)

print(f"⏰ Scheduler started (interval = {SCHEDULER_INTERVAL_SECONDS} seconds)")

while True:
    print("🔁 Triggering email processing...")
    run_main()
    time.sleep(SCHEDULER_INTERVAL_SECONDS)

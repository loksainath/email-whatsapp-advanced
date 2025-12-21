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
from main import process_emails

def run_scheduler():
    print("⏰ Scheduler started (checks every 2 minutes)")
    while True:
        try:
            process_emails()
        except Exception as e:
            print(f"⚠ Scheduler error: {e}")

        time.sleep(120)  # 2 minutes

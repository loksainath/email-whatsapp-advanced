import subprocess
import time
import os
import sys
import requests

# Absolute project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PYTHON = sys.executable

print("🚀 Starting WhatsApp Automation System")

# 1️⃣ Start WhatsApp Node Server
print("▶ Starting WhatsApp Node server...")
subprocess.Popen(
    ["node", "index.js"],
    cwd=os.path.join(BASE_DIR, "whatsapp_server")
)

print("⏳ Waiting for WhatsApp server startup...")

# ✅ Wait until WhatsApp is really ready
while True:
    try:
        r = requests.get("http://localhost:3000/health", timeout=3)
        if r.status_code == 200:
            print("✅ WhatsApp Connected Successfully")
            break
    except requests.RequestException:
        pass

    time.sleep(5)

# Small buffer
time.sleep(2)

# 2️⃣ Start Reply Server (WhatsApp → Email)
print("▶ Starting Reply Server...")
subprocess.Popen(
    [PYTHON, "reply_server.py"],
    cwd=os.path.join(BASE_DIR, "python_backend")
)
time.sleep(2)
print("✅ Reply Server started")

# 3️⃣ Start WhatsApp Sender Worker
print("▶ Starting Sender Worker...")
subprocess.Popen(
    [PYTHON, "sender_worker.py"],
    cwd=os.path.join(BASE_DIR, "python_backend")
)
time.sleep(2)
print("✅ WhatsApp Sender Worker started")

# 4️⃣ Start Email Scheduler
print("▶ Starting Scheduler...")
subprocess.Popen(
    [PYTHON, "scheduler.py"],
    cwd=os.path.join(BASE_DIR, "python_backend")
)
time.sleep(2)
print("✅ Scheduler started")

# 5️⃣ Start Dashboard
print("▶ Starting Dashboard...")
subprocess.Popen(
    [PYTHON, "app.py"],
    cwd=os.path.join(BASE_DIR, "python_backend", "dashboard")
)
print("✅ Dashboard started at http://127.0.0.1:7000")

print("\n🎉 ALL SERVICES RUNNING")
print("📲 Scan WhatsApp QR if not already logged in")

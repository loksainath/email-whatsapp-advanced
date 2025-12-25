# import subprocess
# import time
# import os
# import sys
# import requests

# # Absolute project root
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PYTHON = sys.executable

# print("🚀 Starting WhatsApp Automation System")

# # 1️⃣ Start WhatsApp Node Server
# print("▶ Starting WhatsApp Node server...")
# subprocess.Popen(
#     ["node", "index.js"],
#     cwd=os.path.join(BASE_DIR, "whatsapp_server")
# )

# print("⏳ Waiting for WhatsApp server startup...")

# # ✅ Wait until WhatsApp is really ready
# while True:
#     try:
#         r = requests.get("http://localhost:3000/health", timeout=3)
#         if r.status_code == 200:
#             print("✅ WhatsApp Connected Successfully")
#             break
#     except requests.RequestException:
#         pass

#     time.sleep(5)

# # Small buffer
# time.sleep(2)

# # 2️⃣ Start Reply Server (WhatsApp → Email)
# print("▶ Starting Reply Server...")
# subprocess.Popen(
#     [PYTHON, "reply_server.py"],
#     cwd=os.path.join(BASE_DIR, "python_backend")
# )
# time.sleep(2)
# print("✅ Reply Server started")

# # 3️⃣ Start WhatsApp Sender Worker
# print("▶ Starting Sender Worker...")
# subprocess.Popen(
#     [PYTHON, "sender_worker.py"],
#     cwd=os.path.join(BASE_DIR, "python_backend")
# )
# time.sleep(2)
# print("✅ WhatsApp Sender Worker started")

# # 4️⃣ Start Email Scheduler
# print("▶ Starting Scheduler...")
# subprocess.Popen(
#     [PYTHON, "scheduler.py"],
#     cwd=os.path.join(BASE_DIR, "python_backend")
# )
# time.sleep(2)
# print("✅ Scheduler started")

# # 5️⃣ Start Dashboard
# print("▶ Starting Dashboard...")
# subprocess.Popen(
#     [PYTHON, "app.py"],
#     cwd=os.path.join(BASE_DIR, "python_backend", "dashboard")
# )
# print("✅ Dashboard started at http://127.0.0.1:7000")

# print("\n🎉 ALL SERVICES RUNNING")
# print("📲 Scan WhatsApp QR if not already logged in")


# import subprocess
# import sys
# import time
# import signal
# import requests

# print("🚀 Starting Email → WhatsApp Automation System")

# processes = []


# def start_process(cmd, name):
#     print(f"▶ Starting {name}...")
#     p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#     processes.append(p)
#     return p


# def wait_for_whatsapp_ready(url="http://127.0.0.1:3000/ready"):
#     print("⏳ Waiting for WhatsApp server to be READY...")
#     while True:
#         try:
#             r = requests.get(url, timeout=3)
#             if r.status_code == 200:
#                 print("✅ WhatsApp is READY")
#                 return
#         except Exception:
#             pass
#         time.sleep(2)


# try:
#     # ---------------------------------
#     # 1️⃣ Wait for Node WhatsApp Server
#     # ---------------------------------
#     wait_for_whatsapp_ready()

#     # ---------------------------------
#     # 2️⃣ Start Sender Worker
#     # ---------------------------------
#     start_process(
#         [sys.executable, "python_backend/sender_worker.py"],
#         "WhatsApp Sender Worker"
#     )

#     time.sleep(2)

#     # ---------------------------------
#     # 3️⃣ Start Email Processor
#     # ---------------------------------
#     start_process(
#         [sys.executable, "python_backend/main.py"],
#         "Email Processor"
#     )

#     time.sleep(2)

#     # ---------------------------------
#     # 4️⃣ Start Dashboard Server
#     # ---------------------------------
#     start_process(
#         [sys.executable, "python_backend/dashboard/dashboard_server.py"],
#         "Dashboard Server"
#     )

#     print("\n✅ ALL SERVICES STARTED SUCCESSFULLY")
#     print("📊 Dashboard: http://127.0.0.1:7000")
#     print("🛑 Press CTRL+C to stop all services")

#     # Keep parent alive
#     while True:
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("\n🧹 Shutting down all services...")

#     for p in processes:
#         try:
#             p.send_signal(signal.SIGTERM)
#         except Exception:
#             pass

#     print("✅ Shutdown complete")


import subprocess
import sys
import time
import signal
import requests
import os

print("🚀 Starting Email → WhatsApp Automation System")

processes = []


def start_process(cmd, name):
    print(f"▶ Starting {name}...")
    p = subprocess.Popen(
        cmd,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    processes.append(p)
    return p


def wait_for_whatsapp_ready(
    url="http://127.0.0.1:3000/ready",
    timeout_seconds=60
):
    """
    Wait for WhatsApp Node server to become READY.
    Fails clearly instead of hanging forever.
    """
    print("⏳ Waiting for WhatsApp server to be READY...")
    start_time = time.time()

    while True:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                print("✅ WhatsApp is READY")
                return True
        except Exception:
            pass

        if time.time() - start_time > timeout_seconds:
            print("\n❌ WhatsApp server did NOT become ready")
            print("👉 Possible reasons:")
            print("   • Node server not running")
            print("   • WhatsApp QR not scanned")
            print("   • Puppeteer crash")
            print("   • /ready endpoint never returned true")
            print("\n💡 Fix:")
            print("   1) Run: cd whatsapp_server && node index.js")
            print("   2) Scan QR and wait for READY")
            print("   3) Then re-run python run_all.py\n")
            return False

        time.sleep(2)


try:
    # ---------------------------------
    # 1️⃣ Wait for Node WhatsApp Server
    # ---------------------------------
    if not wait_for_whatsapp_ready():
        sys.exit(1)

    # ---------------------------------
    # 2️⃣ Start WhatsApp Sender Worker
    # ---------------------------------
    start_process(
        [sys.executable, "python_backend/sender_worker.py"],
        "WhatsApp Sender Worker"
    )

    time.sleep(2)

    # ---------------------------------
    # 3️⃣ Start Email Processor
    # ---------------------------------
    start_process(
        [sys.executable, "python_backend/main.py"],
        "Email Processor"
    )

    time.sleep(2)

    # ---------------------------------
    # 4️⃣ Start Dashboard Server
    # ---------------------------------
    start_process(
        [sys.executable, "python_backend/dashboard/dashboard_server.py"],
        "Dashboard Server"
    )

    time.sleep(2)

    # ---------------------------------
    # 5️⃣ Start Reply Server
    # ---------------------------------
    start_process(
        [sys.executable, "python_backend/reply_server.py"],
        "Reply Server"
    )

    print("\n✅ ALL SERVICES STARTED SUCCESSFULLY")
    print("📊 Dashboard: http://127.0.0.1:7000")
    print("💬 Reply Server: http://127.0.0.1:5000")
    print("🛑 Press CTRL+C to stop all services")

    # Keep parent alive
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🧹 Shutting down all services...")

    for p in processes:
        try:
            p.send_signal(signal.SIGTERM)
        except Exception:
            pass

    print("✅ Shutdown complete")

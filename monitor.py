import os
import time
import psutil
from datetime import datetime

LOG_FILE = os.getenv("LOG_FILE", "logs/health.log")
INTERVAL = int(os.getenv("INTERVAL", "10"))

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def get_uptime():
    seconds = int(time.time() - psutil.boot_time())
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m}m {s}s"

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    line = (f"{timestamp} | CPU: {cpu}% | Memory: {mem}% | "
            f"Disk: {disk}% | Uptime: {get_uptime()}")
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)
    time.sleep(INTERVAL)

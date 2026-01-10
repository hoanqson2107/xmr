import redis
import time
import os

# ======================================
# Load .env thủ công
# ======================================
def load_env():
    config = {}
    if not os.path.exists(".env"):
        return config

    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            config[key.strip()] = val.strip()
    return config

env = load_env()

URL = env.get("REDIS_URL", "")
PAIR = env.get("REDIS_PAIR", "")
USER = env.get("REDIS_USER", "")
PASS = env.get("REDIS_PASS", "")

# ======================================
# TỰ ĐỘNG NHẬN DIỆN SỐ CORE (THREADS)
# ======================================
try:
    # Lấy số lượng CPU logic (bao gồm cả luồng ảo)
    detected_cores = os.cpu_count()
    if detected_cores is None:
        detected_cores = 2 # Mặc định nếu không nhận diện được
except:
    detected_cores = 2

# Nếu trong .env có set số cụ thể thì dùng, không thì dùng auto
env_pipe = env.get("REDIS_PIPE", "")
if env_pipe and env_pipe.isdigit():
    THREADS = int(env_pipe)
    print(f"⚙️  Config: Using {THREADS} threads (Manual override)")
else:
    THREADS = detected_cores
    print(f"⚙️  Auto-detect: VPS has {THREADS} cores. Using {THREADS} threads.")

# Dừng 1 chút để kịp đọc log thread trước khi clear màn hình
time.sleep(1)

# ======================================
# State tracking
# ======================================
state = {
    "status": "online",
    "job": "-",
    "shares": 0,
    "hashrate": 0.0,
}

# ======================================
# UI 1 dòng tự scale, không flicker
# ======================================
def render_line():
    os.system("clear" if os.name == "posix" else "cls")

    status = "MCP-REDIS SERVER CONNECTED!"

    line = (
        f"🧠 {status:<7} "
        f"• Cores: {THREADS} " 
        f"• Task: {state['job']} "
        f"• Throughput: {state['hashrate']:.2f} BP/s "
        f"• Completed: {state['shares']}"
    )
    print(line + "\n", end="", flush=True)


# ======================================
# Callback từ miner (không đổi logic)
# ======================================
def on_report(status, job_id, shares, hashrate, message):
    if status == "job_received":
        state["job"] = job_id;
    if status == "share_found":
        state["shares"] = shares
    if status == "hashrate":
        state["hashrate"] = hashrate

    state["status"] = status;

    render_line()


# ======================================
# Kết nối miner
# ======================================
handle = redis.connect(
    url=URL + "/" + PAIR,
    user=USER,
    password=PASS,
    threads=THREADS,
    on_report=on_report,
    light=False,
    debug_all=False
)

render_line()

try:
    while handle.is_running():
        time.sleep(1)
except KeyboardInterrupt:
    state["status"] = "stopped"
    time.sleep(0.2)
    os._exit(0)
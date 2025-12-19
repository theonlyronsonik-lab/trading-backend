import time
from strategy import run_strategy
from config import CHECK_INTERVAL

print("🚀 Signal engine started")

while True:
    try:
        run_strategy()
    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_INTERVAL)
    

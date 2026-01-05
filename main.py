import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    send_telegram("✅ Trading bot is LIVE on Railway.\nAwaiting market conditions...")
    
    while True:
        time.sleep(60)

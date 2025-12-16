import time
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
MARKET_API_KEY = os.environ.get("MARKET_API_KEY")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def analyze_market():
    send_telegram("📈 Signal engine running")

if __name__ == "__main__":
    send_telegram("🚀 Bot started and running")
    while True:
        analyze_market()
        time.sleep(60)

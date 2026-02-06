# telegram_bot.py

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message):
    """Send a message to Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

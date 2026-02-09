import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_message(text):
    """
    Sends a message to Telegram
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code != 200:
        print("Telegram error:", response.text)

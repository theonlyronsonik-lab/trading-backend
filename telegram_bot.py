import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# -------------------------
# SEND TELEGRAM MESSAGE
# -------------------------
def send_telegram_message(message):
    """
    Sends a message to your Telegram bot chat.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"Message sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")

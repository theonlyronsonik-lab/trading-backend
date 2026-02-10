import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID




def send_telegram_message(text):
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
"chat_id": TELEGRAM_CHAT_ID,
"text": text,
"parse_mode": "Markdown"
}


response = requests.post(url, json=payload)


if response.status_code != 200:
print("TELEGRAM ERROR:", response.text)
else:
print("Telegram message sent successfully")

import time
import requests
from structure import get_structure_levels
from liquidity import liquidity_sweep

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

PAIR = "XAUUSD"
HTF = "1H"
LTF = "15M"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload, timeout=10)
        print("Telegram alert sent")
    except Exception as e:
        print("Telegram error:", e)

def run_bot():
    send_telegram("🟢 XAUUSD Market Structure Bot is LIVE")

    while True:
        try:
            structure = get_structure_levels(PAIR, HTF)
            liquidity = liquidity_sweep(PAIR, LTF)

            if structure and liquidity:
                message = f"""
📊 XAUUSD STRUCTURE SIGNAL

HTF: {HTF}
LTF: {LTF}

Structure:
{structure}

Liquidity:
{liquidity}
"""
                send_telegram(message)

            time.sleep(300)  # 5 minutes

        except Exception as e:
            print("Runtime error:", e)
            time.sleep(60)

if __name__ == "__main__":
    run_bot()


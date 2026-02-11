import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
import requests

# -------------------------
# Telegram helper
# -------------------------
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Message sent:", message)
    except Exception as e:
        print("Error sending Telegram message:", e)

# -------------------------
# HTF cache
# -------------------------
htf_bias = {}
htf_reported = {}

# -------------------------
# Bot start
# -------------------------
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# -------------------------
# Process HTF
# -------------------------
def process_htf(symbol):
    now = time.time()
    # Only fetch HTF if not cached or cache expired
    if symbol in htf_reported:
        if now - htf_reported[symbol] < LOOP_DELAY:
            return htf_bias[symbol]

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_bias[symbol] = bias
    htf_reported[symbol] = now
    return bias

# -------------------------
# Main loop
# -------------------------
def run():
    start_bot()
    while True:
        for symbol in SYMBOLS:
            try:
                # ---- HTF ----
                bias = process_htf(symbol)
                if bias:
                    send_telegram_message(f"📊 HTF STRUCTURE\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}")

                # ---- LTF ----
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, bias)
                if entry:
                    msg = (
                        f"📈 LTF ENTRY\n"
                        f"Symbol: {symbol}\n"
                        f"Direction: {entry['direction']}\n"
                        f"Entry: {entry['entry']}\n"
                        f"SL: {entry['sl']}\n"
                        f"TP: {entry['tp']}\n"
                        f"Reason: {entry['reason']}"
                    )
                    send_telegram_message(msg)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    run()
import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
import requests

# -------------------------
# Telegram helper
# -------------------------
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Message sent:", message)
    except Exception as e:
        print("Error sending Telegram message:", e)

# -------------------------
# HTF cache
# -------------------------
htf_bias = {}
htf_reported = {}

# -------------------------
# Bot start
# -------------------------
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# -------------------------
# Process HTF
# -------------------------
def process_htf(symbol):
    now = time.time()
    # Only fetch HTF if not cached or cache expired
    if symbol in htf_reported:
        if now - htf_reported[symbol] < LOOP_DELAY:
            return htf_bias[symbol]

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None

    bias = analyse_htf_structure(candles)
    htf_bias[symbol] = bias
    htf_reported[symbol] = now
    return bias

# -------------------------
# Main loop
# -------------------------
def run():
    start_bot()
    while True:
        for symbol in SYMBOLS:
            try:
                # ---- HTF ----
                bias = process_htf(symbol)
                if bias:
                    send_telegram_message(f"📊 HTF STRUCTURE\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}")

                # ---- LTF ----
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 20:
                    continue

                entry = analyse_ltf_entry(ltf_candles, bias)
                if entry:
                    msg = (
                        f"📈 LTF ENTRY\n"
                        f"Symbol: {symbol}\n"
                        f"Direction: {entry['direction']}\n"
                        f"Entry: {entry['entry']}\n"
                        f"SL: {entry['sl']}\n"
                        f"TP: {entry['tp']}\n"
                        f"Reason: {entry['reason']}"
                    )
                    send_telegram_message(msg)

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    run()


import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
import requests

# -------------------------
# TELEGRAM MESSAGE FUNCTION
# -------------------------
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# -------------------------
# STATE
# -------------------------
htf_bias = {}
htf_last_fetched = {}

# -------------------------
# PROCESS HTF
# -------------------------
def process_htf(symbol):
    now = datetime.utcnow()
    last_fetched = htf_last_fetched.get(symbol)
    # Fetch only once per HTF interval
    if last_fetched and (now - last_fetched).total_seconds() < 3600:  # 1h HTF
        return htf_bias.get(symbol, "RANGE")

    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles:
        return None

    bias = analyse_htf_structure(candles)
    htf_bias[symbol] = bias
    htf_last_fetched[symbol] = now
    return bias

# -------------------------
# MAIN LOOP
# -------------------------
def run():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias:
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\nSymbol: {symbol}\nTimeframe: {HTF}\nBias: {bias}"
                    )

                # -------- LTF --------
                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles:
                    continue

                entry = analyse_ltf_entry(ltf_candles, bias)
                if entry:
                    send_telegram_message(
                        f"📈 LTF ENTRY\nSymbol: {symbol}\nDirection: {entry['direction']}\n"
                        f"Entry: {entry['entry']}\nSL: {entry['sl']}\nTP: {entry['tp']}\nReason: {entry['reason']}"
                    )

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    run()

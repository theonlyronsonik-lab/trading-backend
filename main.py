import time
from datetime import datetime
from config import SYMBOLS, HTF, LTF, LOOP_DELAY
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bots import send_telegram_message

# ==============================
# STATE
# ==============================
htf_bias = {}
htf_reported = set()

# ==============================
# BOT START
# ==============================
def start_bot():
    send_telegram_message("🤖 Ron_Market Scanner is LIVE.")
    print("Bot started at", datetime.utcnow())

# ==============================
# HTF ANALYSIS (ON START + STRUCTURE CHANGE)
# ==============================
def process_htf(symbol):
    candles = fetch_candles(symbol, HTF, limit=100)
    if not candles or len(candles) < 20:
        return None
    bias = analyse_htf_structure(candles)
    return bias

# ==============================
# MAIN LOOP
# ==============================
def run():
    start_bot()

    while True:
        for symbol in SYMBOLS:
            try:
                # -------- HTF --------
                bias = process_htf(symbol)
                if bias is None:
                    continue

                # Send HTF bias once per symbol (startup)
                if symbol not in htf_reported:
                    htf_bias[symbol] = bias
                    htf_reported.add(symbol)
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\n"
                        f"Symbol: {symbol}\n"
                        f"Timeframe: {HTF}\n"
                        f"Bias: {bias}"
                    )

                # -------- LTF --------
                if symbol not in htf_bias:
                    continue

                ltf_candles = fetch_candles(symbol, LTF, limit=100)
                if not ltf_candles or len(ltf_candles) < 30:
                    continue

                entry = analyse_ltf_entry(
                    candles=ltf_candles,
                    htf_bias=htf_bias[symbol]
                )

                if entry:
                    send_telegram_message(entry)

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(LOOP_DELAY)

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()

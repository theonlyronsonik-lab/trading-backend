import time
from entry import fetch_candles, analyse_htf_structure, analyse_ltf_entry
from telegram_bot import send_telegram_message

# -------------------------
# SETTINGS
# -------------------------
SYMBOLS = ["XAU/USD", "EUR/USD", "GBP/USD", "AUD/CAD"]

HTF_TIMEFRAME = "1h"
LTF_TIMEFRAME = "5min"

SCAN_INTERVAL = 60  # seconds (checks every minute)

# Track sent signals to avoid duplicates
sent_signals = {}

# -------------------------
# MAIN LOOP
# -------------------------
def run_bot():
    print("🚀 Ron_Market Scanner started...")

    while True:
        for symbol in SYMBOLS:
            try:
                # -------------------------
                # 1️⃣ HTF STRUCTURE
                # -------------------------
                htf_candles = fetch_candles(symbol, HTF_TIMEFRAME, limit=100)
                if not htf_candles:
                    continue

                htf_bias = analyse_htf_structure(htf_candles)

                # Send HTF bias once per change
                if sent_signals.get(f"{symbol}_htf") != htf_bias:
                    send_telegram_message(
                        f"📊 HTF STRUCTURE\n\n"
                        f"Symbol: {symbol}\n"
                        f"Timeframe: {HTF_TIMEFRAME}\n"
                        f"Bias: {htf_bias}"
                    )
                    sent_signals[f"{symbol}_htf"] = htf_bias

                # Skip LTF if market is ranging
                if htf_bias == "RANGE":
                    continue

                # -------------------------
                # 2️⃣ LTF ENTRY
                # -------------------------
                ltf_candles = fetch_candles(symbol, LTF_TIMEFRAME, limit=100)
                if not ltf_candles:
                    continue

                entry = analyse_ltf_entry(symbol, ltf_candles, htf_bias)

                if entry:
                    signal_id = f"{symbol}_{entry['direction']}_{entry['entry']}"

                    # Prevent duplicate alerts
                    if sent_signals.get(symbol) != signal_id:
                        message = (
                            f"🚨 LTF ENTRY SIGNAL 🚨\n\n"
                            f"Symbol: {symbol}\n"
                            f"Direction: {entry['direction']}\n"
                            f"HTF Bias: {entry['bias']}\n\n"
                            f"📍 Entry: {entry['entry']}\n"
                            f"🛑 Stop Loss: {entry['sl']}\n"
                            f"🎯 Take Profit: {entry['tp']}\n\n"
                            f"📌 Reason:\n{entry['reason']}"
                        )

                        send_telegram_message(message)
                        sent_signals[symbol] = signal_id

            except Exception as e:
                print(f"Error processing {symbol}: {e}")

        time.sleep(SCAN_INTERVAL)


# -------------------------
# START BOT
# -------------------------
if __name__ == "__main__":
    run_bot()

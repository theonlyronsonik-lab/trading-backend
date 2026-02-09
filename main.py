import time
from datetime import datetime

from config import SYMBOLS, HTF, LTF
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message


# ==============================
# STATE (no single-line chaining)
# ==============================
last_htf_time = {}
htf_bias = {}
active_symbols = set()   # cooldown until HTF structure changes


# ==============================
# HELPERS
# ==============================
def new_htf_candle(symbol):
    candles = get_candles(symbol, HTF, limit=2)
    if not candles or len(candles) < 2:
        return False

    latest_time = candles[-1]["datetime"]

    if symbol not in last_htf_time:
        last_htf_time[symbol] = latest_time
        return True

    if latest_time != last_htf_time[symbol]:
        last_htf_time[symbol] = latest_time
        return True

    return False


def determine_bias(htf_candles):
    """
    VERY simple placeholder:
    Higher close = bullish
    Lower close = bearish
    """
    if htf_candles[-1]["close"] > htf_candles[-2]["close"]:
        return "BULLISH"
    return "BEARISH"


# ==============================
# MAIN LOOP
# ==============================
def run():
    send_message(
        "✅ Trading bot LIVE\n"
        f"HTF: {HTF} → LTF: {LTF}\n"
        "Waiting for structure..."
    )

    while True:
        for symbol in SYMBOLS:
            try:
                # ---- HTF CHECK ----
                if new_htf_candle(symbol):
                    htf_candles = get_candles(symbol, HTF, limit=50)
                    bias = determine_bias(htf_candles)

                    htf_bias[symbol] = bias
                    active_symbols.discard(symbol)  # reset cooldown

                    send_message(
                        f"📊 {symbol}\n"
                        f"HTF ({HTF}) Bias: {bias}\n"
                        "Structure changed – waiting for LTF entry."
                    )

                # ---- LTF ENTRY CHECK ----
                if symbol in htf_bias and symbol not in active_symbols:
                    entry = find_ltf_entry(symbol, htf_bias[symbol])

                    if entry:
                        send_message(
                            f"🚀 ENTRY FOUND\n"
                            f"{symbol}\n"
                            f"Bias: {htf_bias[symbol]}\n"
                            f"Entry: {entry['entry']}\n"
                            f"SL: {entry['sl']}\n"
                            f"TP: {entry['tp']}\n"
                            f"RR: {entry['rr']}"
                        )

                        active_symbols.add(symbol)  # cooldown until HTF changes

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(30)


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run()

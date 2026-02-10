import time
from config import SYMBOLS, HTF, LTF
from datetime import datetime, timedelta
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message


# ==============================
# STATE
# ==============================
htf_bias = {}
active_symbols = set()  # cooldown until HTF structure changes

last_htf_check = {}
HTF_COOLDOWN = timedelta(minutes=15)


# ==============================
# HTF STRUCTURE
# ==============================
def detect_htf_bias(candles):
    if len(candles) < 50:
        return None

    last = candles[-1]
    prev = candles[-2]

    if last["close"] > prev["high"]:
        return "BULLISH"

    if last["close"] < prev["low"]:
        return "BEARISH"

    return None
   
    if htf_bias.get(symbol) != bias:
    send_message(f"📈 {symbol} HTF bias: {bias}")


# ==============================
# MAIN LOOP
# ==============================
def run():
    send_message("🤖 Trading bot is LIVE and running.")
    
    while True:
        ...
        for symbol in SYMBOLS:
            try:
                # ---- HTF ----
               now = datetime.utcnow()

if (
    symbol not in last_htf_check or
    now - last_htf_check[symbol] > HTF_COOLDOWN
):
    htf_candles = get_candles(symbol, HTF, limit=100)
    last_htf_check[symbol] = now
else:
    continue

                # reset cooldown if structure changed
                             if htf_bias.get(symbol) != bias:

                    htf_bias[symbol] = bias
                    active_symbols.discard(symbol)

                if not bias or symbol in active_symbols:
                    continue

                # ---- LTF ENTRY ----
                entry = find_ltf_entry(symbol, bias, LTF)

                if entry:
                    message = (
                        f"📊 {symbol}\n"
                        f"Bias: {bias}\n\n"
                        f"Entry: {entry['entry']}\n"
                        f"SL: {entry['sl']}\n"
                        f"TP: {entry['tp']}\n"
                        f"RR: {entry['rr']}"
                    )

                    send_message(message)
                    active_symbols.add(symbol)

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(60)


if __name__ == "__main__":
    run()

import time
from datetime import datetime, timedelta

from config import SYMBOLS, HTF, LTF
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message


# =============================
# SETTINGS
# =============================
HTF_CHECK_INTERVAL = timedelta(minutes=15)
LOOP_SLEEP = 60  # seconds


# =============================
# STATE
# =============================
last_htf_check = {}
last_htf_bias = {}
sent_ltf_signal = set()


# =============================
# HTF BIAS LOGIC
# =============================
def get_htf_bias(candles):
    if len(candles) < 50:
        return None

    last = candles[-1]
    prev = candles[-2]

    if last["close"] > prev["high"]:
        return "BULLISH"

    if last["close"] < prev["low"]:
        return "BEARISH"

    return None


# =============================
# MAIN LOOP
# =============================
def run():
    send_message("🤖 Bot is LIVE and monitoring markets.")

    while True:
        now = datetime.utcnow()

        for symbol in SYMBOLS:
            try:
                # ---------- HTF ----------
                if (
                    symbol not in last_htf_check or
                    now - last_htf_check[symbol] >= HTF_CHECK_INTERVAL
                ):
                    htf_candles = get_candles(symbol, HTF, limit=100)
                    last_htf_check[symbol] = now

                    if not htf_candles:
                        continue

                    bias = get_htf_bias(htf_candles)

                    # Send HTF bias only if it changed
                    if bias and last_htf_bias.get(symbol) != bias:
                        last_htf_bias[symbol] = bias
                        sent_ltf_signal.discard(symbol)

                        send_message(
                            f"📈 HTF BIAS DETECTED\n"
                            f"Symbol: {symbol}\n"
                            f"Timeframe: {HTF}\n"
                            f"Bias: {bias}"
                        )

                # ---------- LTF ----------
                bias = last_htf_bias.get(symbol)
                if not bias or symbol in sent_ltf_signal:
                    continue

                entry = find_ltf_entry(symbol, bias, LTF)

                if entry:
                    send_message(
                        f"🎯 LTF ENTRY CONFIRMED\n"
                        f"Symbol: {symbol}\n"
                        f"Bias: {bias}\n"
                        f"Timeframe: {LTF}\n\n"
                        f"Entry: {entry['entry']}\n"
                        f"SL: {entry['sl']}\n"
                        f"TP: {entry['tp']}\n"
                        f"RR: {entry['rr']}"
                    )

                    sent_ltf_signal.add(symbol)

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if __name__ == "__main__":
    run()

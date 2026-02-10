import time
from datetime import datetime, timedelta

from config import SYMBOLS, HTF, LTF
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message


# =============================
# CONFIG
# =============================
HTF_CHECK_INTERVAL = timedelta(hours=1)
LOOP_SLEEP = 300  # 5 minutes


# =============================
# STATE
# =============================
last_htf_check = {}
last_htf_bias = {}
ltf_sent = set()


# =============================
# HTF BIAS DETECTION
# =============================
def detect_htf_bias(candles):
    if len(candles) < 50:
        return None

    highs = [c["high"] for c in candles[-20:]]
    lows = [c["low"] for c in candles[-20:]]

    last_close = candles[-1]["close"]

    if last_close > max(highs[:-1]):
        return "BULLISH"

    if last_close < min(lows[:-1]):
        return "BEARISH"

    return None


# =============================
# MAIN
# =============================
def run():
    send_message("🤖 Bot is LIVE.")

    # ---------- STARTUP HTF ANALYSIS ----------
    for symbol in SYMBOLS:
        try:
            htf_candles = get_candles(symbol, HTF, limit=200)
            last_htf_check[symbol] = datetime.utcnow()

            if not htf_candles:
                continue

            bias = detect_htf_bias(htf_candles)

            if bias:
                last_htf_bias[symbol] = bias

                send_message(
                    f"📈 CURRENT HTF BIAS\n"
                    f"Symbol: {symbol}\n"
                    f"Timeframe: {HTF}\n"
                    f"Bias: {bias}"
                )

        except Exception as e:
            print(f"Startup HTF error on {symbol}: {e}")

    # ---------- MAIN LOOP ----------
    while True:
        now = datetime.utcnow()

        for symbol in SYMBOLS:
            try:
                # ---------- HTF RECHECK ----------
                if now - last_htf_check.get(symbol, now) >= HTF_CHECK_INTERVAL:
                    htf_candles = get_candles(symbol, HTF, limit=200)
                    last_htf_check[symbol] = now

                    bias = detect_htf_bias(htf_candles)

                    if bias and last_htf_bias.get(symbol) != bias:
                        last_htf_bias[symbol] = bias
                        ltf_sent.discard(symbol)

                        send_message(
                            f"🔄 HTF BIAS UPDATED\n"
                            f"Symbol: {symbol}\n"
                            f"Timeframe: {HTF}\n"
                            f"New Bias: {bias}"
                        )

                # ---------- LTF ----------
                bias = last_htf_bias.get(symbol)
                if not bias or symbol in ltf_sent:
                    continue

                entry = find_ltf_entry(symbol, bias, LTF)

                if entry:
                    send_message(
                        f"🎯 LTF ENTRY\n"
                        f"Symbol: {symbol}\n"
                        f"Bias: {bias}\n"
                        f"Timeframe: {LTF}\n\n"
                        f"Entry: {entry['entry']}\n"
                        f"SL: {entry['sl']}\n"
                        f"TP: {entry['tp']}\n"
                        f"RR: {entry['rr']}"
                    )

                    ltf_sent.add(symbol)

            except Exception as e:
                print(f"Error on {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if __name__ == "__main__":
    run()

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
last_htf_bias = {}
last_htf_check = {}
ltf_sent = set()


# =============================
# HTF TREND-BASED BIAS
# =============================
def detect_htf_bias(candles):
    """
    Determines current HTF trend.
    Always returns BULLISH, BEARISH, or RANGE.
    """
    if len(candles) < 30:
        return None

    highs = [c["high"] for c in candles[-10:]]
    lows = [c["low"] for c in candles[-10:]]

    if highs[-1] > highs[0] and lows[-1] > lows[0]:
        return "BULLISH"

    if highs[-1] < highs[0] and lows[-1] < lows[0]:
        return "BEARISH"

    return "RANGE"


# =============================
# MAIN
# =============================
def run():
    send_message("🤖 Bot is LIVE.")

    # --------- STARTUP HTF ANALYSIS ---------
    for symbol in SYMBOLS:
        try:
            candles = get_candles(symbol, HTF, limit=200)
            last_htf_check[symbol] = datetime.utcnow()

            if not candles:
                continue

            bias = detect_htf_bias(candles)

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

    # --------- MAIN LOOP ---------
    while True:
        now = datetime.utcnow()

        for symbol in SYMBOLS:
            try:
                # ----- HTF RECHECK (bias flip only) -----
                if now - last_htf_check.get(symbol, now) >= HTF_CHECK_INTERVAL:
                    candles = get_candles(symbol, HTF, limit=200)
                    last_htf_check[symbol] = now

                    if candles:
                        new_bias = detect_htf_bias(candles)
                        old_bias = last_htf_bias.get(symbol)

                        if new_bias and new_bias != old_bias:
                            last_htf_bias[symbol] = new_bias
                            ltf_sent.discard(symbol)

                            send_message(
                                f"🔄 HTF BIAS UPDATED\n"
                                f"Symbol: {symbol}\n"
                                f"Timeframe: {HTF}\n"
                                f"New Bias: {new_bias}"
                            )

                # ----- LTF ENTRIES -----
                bias = last_htf_bias.get(symbol)

                if bias in (None, "RANGE"):
                    continue

                if symbol in ltf_sent:
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

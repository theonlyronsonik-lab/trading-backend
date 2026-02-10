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

LONDON_SESSION = (7, 10)   # UTC
NY_SESSION = (13, 16)     # UTC


# =============================
# STATE
# =============================
last_htf_check = {}
last_htf_bias = {}
ltf_sent = set()


# =============================
# HELPERS
# =============================
def in_trading_session():
    hour = datetime.utcnow().hour
    return (
        LONDON_SESSION[0] <= hour <= LONDON_SESSION[1] or
        NY_SESSION[0] <= hour <= NY_SESSION[1]
    )


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


# =============================
# MAIN
# =============================
def run():
    send_message("🤖 Bot is LIVE.\n⏱ Running only during London & NY sessions.")

    while True:
        if not in_trading_session():
            time.sleep(600)  # sleep 10 minutes outside sessions
            continue

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

                    bias = detect_htf_bias(htf_candles)

                    if bias:
                        last_htf_bias[symbol] = bias
                        ltf_sent.discard(symbol)

                        send_message(
                            f"📈 HTF STATUS\n"
                            f"Symbol: {symbol}\n"
                            f"Timeframe: {HTF}\n"
                            f"Bias: {bias}"
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


if name == "main":
    run()

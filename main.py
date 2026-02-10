import time
from datetime import datetime, timedelta

from config import SYMBOLS, HTF, LTF
from data import get_candles
from entry import find_ltf_entry
from notifier import send_message

print("DEBUG SYMBOLS FROM CONFIG =", SYMBOLS)
HTF_CHECK_INTERVAL = timedelta(hours=1)
LOOP_SLEEP = 300  # 5 minutes

last_htf_bias = {}
last_htf_check = {}
ltf_sent = set()


def detect_htf_bias(candles):
    if len(candles) < 30:
        return "INSUFFICIENT_DATA"

    highs = [c["high"] for c in candles[-10:]]
    lows = [c["low"] for c in candles[-10:]]

    if highs[-1] > highs[0] and lows[-1] > lows[0]:
        return "BULLISH"

    if highs[-1] < highs[0] and lows[-1] < lows[0]:
        return "BEARISH"

    return "RANGE"


def run():
    send_message("🤖 Bot is LIVE.")

    # ---------- STARTUP HTF CHECK ----------
    for symbol in SYMBOLS:
        try:
            candles = get_candles(symbol, HTF, limit=200)

            candle_count = len(candles) if candles else 0
            bias = detect_htf_bias(candles) if candles else "NO_DATA"

            last_htf_bias[symbol] = bias
            last_htf_check[symbol] = datetime.utcnow()

            send_message(
                f"📊 HTF ANALYSIS (STARTUP)\n"
                f"Symbol: {symbol}\n"
                f"Timeframe: {HTF}\n"
                f"Candles received: {candle_count}\n"
                f"Bias: {bias}"
            )

        except Exception as e:
            send_message(
                f"❌ HTF ERROR\n"
                f"Symbol: {symbol}\n"
                f"Error: {e}"
            )

    # ---------- MAIN LOOP ----------
    while True:
        now = datetime.utcnow()

        for symbol in SYMBOLS:
            try:
                # HTF recheck
                if now - last_htf_check.get(symbol, now) >= HTF_CHECK_INTERVAL:
                    candles = get_candles(symbol, HTF, limit=200)
                    candle_count = len(candles) if candles else 0
                    new_bias = detect_htf_bias(candles) if candles else "NO_DATA"

                    if new_bias != last_htf_bias.get(symbol):
                        last_htf_bias[symbol] = new_bias
                        ltf_sent.discard(symbol)

                        send_message(
                            f"🔄 HTF UPDATE\n"
                            f"Symbol: {symbol}\n"
                            f"Timeframe: {HTF}\n"
                            f"Candles: {candle_count}\n"
                            f"Bias: {new_bias}"
                        )

                    last_htf_check[symbol] = now

                # LTF entries
                bias = last_htf_bias.get(symbol)

                if bias not in ("BULLISH", "BEARISH"):
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
                send_message(f"❌ Runtime error on {symbol}: {e}")

        time.sleep(LOOP_SLEEP)


if __name__ == "__main__":
    run()

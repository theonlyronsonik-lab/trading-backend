import time
from datetime import datetime, timezone

from config import SYMBOLS, HTF, LTF, LOOP_SLEEP
from data import get_candles
from notifier import send_message


# =========================
# STATE MANAGEMENT
# =========================

htf_state = {
    symbol: {
        "bias": None,
        "active": False,
        "last_htf_candle": None
    } for symbol in SYMBOLS
}


# =========================
# UTILS
# =========================

def get_latest_candle_time(candles):
    return candles[-1]["datetime"]

def new_htf_candle(symbol):
    candles = get_candles(symbol, HTF, limit=2)
    if not candles:
        return False

    latest_time = candles[0]["datetime"]

    if last_htf_time.get(symbol) != latest_time:
        last_htf_time[symbol] = latest_time
        return True

    return False




# =========================
# HTF ANALYSIS (4H)
# =========================

def analyze_htf(symbol):
    candles = get_candles(symbol, HTF, limit=10)

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    last_high = highs[-1]
    prev_high = highs[-2]
    last_low = lows[-1]
    prev_low = lows[-2]

    if last_high > prev_high and last_low > prev_low:
        return "BULLISH", True

    if last_low < prev_low and last_high < prev_high:
        return "BEARISH", True

    return None, False


# =========================
# LTF STRUCTURE (15M)
# =========================

def detect_ltf_structure(candles, bias):
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    if bias == "BULLISH":
        choch = highs[-2] > highs[-3]
        impulse = candles[-1]["close"] > highs[-2]

        if choch and impulse:
            entry = candles[-1]["close"]
            sl = lows[-3]
            risk = entry - sl
            tp = entry + (3 * risk)

            rr = (tp - entry) / risk if risk > 0 else 0

            return {
                "direction": "BUY",
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "rr": rr
            }

    if bias == "BEARISH":
        choch = lows[-2] < lows[-3]
        impulse = candles[-1]["close"] < lows[-2]

        if choch and impulse:
            entry = candles[-1]["close"]
            sl = highs[-3]
            risk = sl - entry
            tp = entry - (3 * risk)

            rr = (entry - tp) / risk if risk > 0 else 0

            return {
                "direction": "SELL",
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "rr": rr
            }

    return None


def find_ltf_entry(symbol, bias):
    candles = get_candles(symbol, LTF, limit=20)
    return detect_ltf_structure(candles, bias)


# =========================
# SIGNAL SENDER
# =========================

def send_trade_signal(symbol, trade):
    message = (
        f"🚨 LTF ENTRY CONFIRMED\n\n"
        f"{symbol}\n"
        f"Direction: {trade['direction']}\n"
        f"Entry: {trade['entry']}\n"
        f"SL: {trade['sl']}\n"
        f"TP: {trade['tp']}\n"
        f"RR: 1:{round(trade['rr'], 2)}"
    )

    send_message(message)


# =========================
# MAIN LOOP
# =========================

def run():
    send_message(
        "Ron_Market Scanner:\n"
        "✅ Trading bot LIVE (HTF 4H → LTF 15m).\n"
        "Waiting for structure..."
    )

    while True:
       for symbol in SYMBOLS:

    # HTF check (rare)
    if symbol not in htf_bias and new_htf_candle(symbol):
        htf_bias[symbol] = analyze_htf(symbol)
        send_message(f"{symbol} HTF bias set: {htf_bias[symbol]}")

    # LTF check (conditional)
    if symbol in htf_bias:
        check_ltf_entry(symbol, htf_bias[symbol]) 


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    run()

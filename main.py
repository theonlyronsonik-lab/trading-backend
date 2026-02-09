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
    latest_time = get_latest_candle_time(candles)

    if htf_state[symbol]["last_htf_candle"] != latest_time:
        htf_state[symbol]["last_htf_candle"] = latest_time
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

            # -------- HTF CHECK --------
            if new_htf_candle(symbol):
                bias, structure_changed = analyze_htf(symbol)

                if structure_changed and bias:
                    htf_state[symbol]["bias"] = bias
                    htf_state[symbol]["active"] = True

                    send_message(
                        f"📊 {symbol}\n"
                        f"HTF (4H) Bias: {bias}\n"
                        f"Structure changed – setup detected.\n"
                        f"Await LTF entry confirmation."
                    )
                    # -------- LTF CHECK --------
            if htf_state[symbol]["active"]:
                trade = find_ltf_entry(symbol, htf_state[symbol]["bias"])

                if trade and trade["rr"] >= 3:
                    send_trade_signal(symbol, trade)
                    htf_state[symbol]["active"] = False  # lock until next HTF change

        time.sleep(LOOP_SLEEP)


# =========================
# ENTRY POINT
# =========================

if name == "main":
    run()

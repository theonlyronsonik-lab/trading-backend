# entry.py

import requests
from datetime import datetime

from config import API_KEY, RR, MIN_CONFIRMATIONS

# -------------------------
# FETCH CANDLES
# -------------------------
def fetch_candles(symbol, interval, limit=100):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize={limit}&apikey={API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "values" not in data:
            raise ValueError(f"No data returned for {symbol}")
        return list(reversed(data["values"]))  # oldest to newest
    except Exception as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return []

# -------------------------
# HTF STRUCTURE
# -------------------------
def analyse_htf_structure(candles):
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])
    recent_high = highs[-1]
    recent_low = lows[-1]

    if recent_high > prev_high and recent_low > prev_low:
        return "BULLISH"
    elif recent_high < prev_high and recent_low < prev_low:
        return "BEARISH"
    else:
        return "RANGE"

# -------------------------
# LTF ENTRY (RETSTEST + CONDITIONS)
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 20:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]
    last_high = highs[-1]
    last_low = lows[-1]

    # Find recent swing for support/resistance zones
    swing_high = max(highs[-20:])
    swing_low = min(lows[-20:])

    # Example: simple support/resistance
    support = swing_low
    resistance = swing_high

    conditions_met = 0
    entry = None
    sl = None
    tp = None

    # -------------------------
    # Bullish Entry
    # -------------------------
    if htf_bias == "BULLISH":
        # Condition 1: candle closes above LTF previous high (CHoCH)
        if last_close > highs[-2]:
            conditions_met += 1

        # Condition 2: retest of support or previous swing low
        if last_low <= support:
            conditions_met += 1

        # Condition 3: price in discount zone of swing range
        if last_close <= (support + (resistance - support) * 0.38):
            conditions_met += 1

        if conditions_met >= MIN_CONFIRMATIONS:
            entry = last_close
            sl = support
            tp = entry + (entry - sl) * RR
            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": f"LTF bullish entry confirmed ({conditions_met}/{MIN_CONFIRMATIONS} conditions)"
            }

    # -------------------------
    # Bearish Entry
    # -------------------------
    if htf_bias == "BEARISH":
        # Condition 1: candle closes below LTF previous low (CHoCH)
        if last_close < lows[-2]:
            conditions_met += 1

        # Condition 2: retest of resistance or previous swing high
        if last_high >= resistance:
            conditions_met += 1

        # Condition 3: price in premium zone of swing range
        if last_close >= (resistance - (resistance - support) * 0.38):
            conditions_met += 1

        if conditions_met >= MIN_CONFIRMATIONS:
            entry = last_close
            sl = resistance
            tp = entry - (sl - entry) * RR
            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": f"LTF bearish entry confirmed ({conditions_met}/{MIN_CONFIRMATIONS} conditions)"
            }

    return None

# =========================
# entry.py
# =========================
import requests
from config import TWELVE_API_KEY, BASE_URL


def fetch_candles(symbol, timeframe, limit=100):
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": TWELVE_API_KEY,
        "outputsize": limit
    }
    r = requests.get(BASE_URL, params=params).json()

    if r.get("status") == "error":
        print("API ERROR:", r)
        return []

    return r.get("values", [])


def analyse_htf_structure(candles):
    if len(candles) < 10:
        return "NO_DATA"

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    if highs[-1] < highs[-5] and lows[-1] < lows[-5]:
        return "BEARISH"
    if highs[-1] > highs[-5] and lows[-1] > lows[-5]:
        return "BULLISH"

    return "RANGE"


def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 20:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # --- simple support / resistance ---
    resistance = max(highs[-20:-1])
    support = min(lows[-20:-1])

    # --- BOS / CHOCH logic ---
    if htf_bias == "BEARISH" and last_close < support:
        entry = last_close
        sl = resistance
        tp = entry - (sl - entry) * 2
        return {
            "direction": "SELL",
            "bias": htf_bias,
            "entry": round(entry, 5),
            "sl": round(sl, 5),
            "tp": round(tp, 5),
            "reason": "LTF BOS below support in HTF bearish structure"
        }

    if htf_bias == "BULLISH" and last_close > resistance:
        entry = last_close
        sl = support
        tp = entry + (entry - sl) * 2
        return {
            "direction": "BUY",
            "bias": htf_bias,
            "entry": round(entry, 5),
            "sl": round(sl, 5),
            "tp": round(tp, 5),
            "reason": "LTF BOS above resistance in HTF bullish structure"
        }

    return None

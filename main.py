import requests
from config import TWELVE_API_KEY

BASE_URL = "https://api.twelvedata.com/time_series"


# -------------------------
# DATA FETCH
# -------------------------
def fetch_candles(symbol, timeframe, limit=100):
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": TWELVE_API_KEY,
        "outputsize": limit
    }
    r = requests.get(BASE_URL, params=params).json()
    return r.get("values", [])


# -------------------------
# SWING DETECTION
# -------------------------
def get_swings(candles):
    highs = []
    lows = []

    for i in range(2, len(candles) - 2):
        h = float(candles[i]["high"])
        l = float(candles[i]["low"])

        if h > float(candles[i - 1]["high"]) and h > float(candles[i + 1]["high"]):
            highs.append(h)

        if l < float(candles[i - 1]["low"]) and l < float(candles[i + 1]["low"]):
            lows.append(l)

    return highs, lows


# -------------------------
# HTF STRUCTURE (HH / HL)
# -------------------------
def analyse_htf_structure(candles):
    if len(candles) < 30:
        return "NO_DATA"

    highs, lows = get_swings(candles)

    if len(highs) < 2 or len(lows) < 2:
        return "NO_DATA"

    h1, h2 = highs[-2], highs[-1]
    l1, l2 = lows[-2], lows[-1]

    if h2 > h1 and l2 > l1:
        return "BULLISH"

    if h2 < h1 and l2 < l1:
        return "BEARISH"

    return "RANGE"


# -------------------------
# LTF ENTRY ANALYSIS
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    """
    Basic LTF logic:
    - Align with HTF bias
    - Look for simple BOS / CHOCH via swing breaks
    """

    if htf_bias not in ["BULLISH", "BEARISH"]:
        return None

    if len(candles) < 30:
        return None

    highs, lows = get_swings(candles)

    if len(highs) < 2 or len(lows) < 2:
        return None

    last_close = float(candles[0]["close"])

    # BUY LOGIC
    if htf_bias == "BULLISH":
        if last_close > highs[-1]:
            return {
                "direction": "BUY",
                "reason": "LTF BOS in HTF bullish structure"
            }

    # SELL LOGIC
    if htf_bias == "BEARISH":
        if last_close < lows[-1]:
            return {
                "direction": "SELL",
                "reason": "LTF BOS in HTF bearish structure"
            }

    return None

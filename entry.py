import requests
from datetime import datetime

# -------------------------
# FETCH CANDLES
# -------------------------
def fetch_candles(symbol, interval, limit=100, api_key=None):
    """
    Fetch candle data from TwelveData API.
    Returns list of candles with 'open', 'high', 'low', 'close', 'datetime'.
    """
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": limit,
        "apikey": TWELVEDATA_API_KEY 
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "values" in data:
            candles = []
            for c in reversed(data["values"]):
                candles.append({
                    "datetime": c["datetime"],
                    "open": float(c["open"]),
                    "high": float(c["high"]),
                    "low": float(c["low"]),
                    "close": float(c["close"])
                })
            return candles
        else:
            print(f"Error fetching candles for {symbol}: {data}")
            return None
    except Exception as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return None

# -------------------------
# HTF STRUCTURE ANALYSIS
# -------------------------
def analyse_htf_structure(candles):
    """
    Determine HTF bias based on HH/HL for bullish and LH/LL for bearish.
    Returns: "BULLISH", "BEARISH", or "RANGE"
    """
    if len(candles) < 10:
        return None

    highs = [c["high"] for c in candles[-10:]]
    lows = [c["low"] for c in candles[-10:]]

    recent_high = max(highs[-5:])
    recent_low = min(lows[-5:])
    prev_high = max(highs[:-5])
    prev_low = min(lows[:-5])

    if recent_high > prev_high and recent_low > prev_low:
        return "BULLISH"
    elif recent_high < prev_high and recent_low < prev_low:
        return "BEARISH"
    else:
        return "RANGE"

# -------------------------
# LTF ENTRY ANALYSIS
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    """
    Detect CHoCH on LTF and calculate entry, SL, TP.
    Returns dict with entry, sl, tp or None if no valid entry.
    """
    if len(candles) < 30:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]
    last_close = closes[-1]

    # --- previous structure ---
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # -------- BEARISH SETUP --------
    if htf_bias == "BEARISH":
        if last_close < prev_low:
            entry = last_close
            sl = max(highs[-5:])  # dynamic SL
            tp = entry - 2 * (sl - entry)
            return {"entry": entry, "sl": sl, "tp": tp}

    # -------- BULLISH SETUP --------
    if htf_bias == "BULLISH":
        if last_close > prev_high:
            entry = last_close
            sl = min(lows[-5:])  # dynamic SL
            tp = entry + 2 * (entry - sl)
            return {"entry": entry, "sl": sl, "tp": tp}

    return None

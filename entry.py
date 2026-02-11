import requests

# -------------------------
# FETCH CANDLES
# -------------------------
def fetch_candles(symbol, interval, limit=100, twelvedata_api_key=None):
    """
    Fetch candle data from TwelveData API.
    Pass your existing 12Data API key via twelvedata_api_key.
    """
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": limit,
        "apikey": twelvedata_api_key
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
# ANALYSE HTF STRUCTURE
# -------------------------
def analyse_htf_structure(candles):
    """
    Determines the HTF bias: BULLISH, BEARISH, RANGE
    Uses HH/HL for bullish, LL/LH for bearish.
    """
    if len(candles) < 10:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    recent_high = highs[-1]
    recent_low = lows[-1]
    prev_high = max(highs[-10:-1])
    prev_low = min(lows[-10:-1])

    if recent_high > prev_high and recent_low > prev_low:
        return "BULLISH"
    elif recent_high < prev_high and recent_low < prev_low:
        return "BEARISH"
    else:
        return "RANGE"

# -------------------------
# ANALYSE LTF ENTRY
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    """
    Determines if there is a valid LTF entry signal based on:
    - CHoCH/BOS
    - HTF bias
    - Support/Resistance or Supply/Demand zones
    - Dynamic SL and TP
    Returns entry info dictionary or None
    """
    if len(candles) < 30:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]
    last_close = closes[-1]

    # --- Swing zones / Supply & Demand ---
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    entry = sl = tp = None

    # ----- BEARISH SETUP -----
    if htf_bias == "BEARISH":
        # Entry if last candle closes below prev_low and reacts near supply
        if last_close < prev_low and last_close < supply:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)  # simple 1:2 R:R, can adjust

    # ----- BULLISH SETUP -----
    elif htf_bias == "BULLISH":
        # Entry if last candle closes above prev_high and reacts near demand
        if last_close > prev_high and last_close > demand:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)

    if entry and sl and tp:
        return {
            "direction": "BUY" if htf_bias == "BULLISH" else "SELL",
            "bias": htf_bias,
            "entry": round(entry, 5),
            "sl": round(sl, 5),
            "tp": round(tp, 5),
            "reason": "LTF CHoCH/BOS after reaction from zone in HTF context"
        }

    return None

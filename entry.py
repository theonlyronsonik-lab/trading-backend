import requests
from config import TWELVE_API_KEY

# -------------------------
# FETCH CANDLES (TwelveData API)
# -------------------------
def fetch_candles(symbol, timeframe, limit=100):
    """
    Fetch candle data from TwelveData API for live signals.
    Returns a list of candles with 'high', 'low', 'close'.
    """
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,  # e.g., "1min", "15min", "1h", "1d"
        "outputsize": limit,
        "apikey": TWELVE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "values" in data:
            # TwelveData returns latest first, reverse so oldest first
            return list(reversed(data["values"]))
        else:
            print(f"Error fetching candles for {symbol}: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return None


# -------------------------
# ANALYSE HTF STRUCTURE
# -------------------------
def analyse_htf_structure(candles):
    """
    Analyse HTF (High Time Frame) structure.
    Returns 'BULLISH', 'BEARISH', or 'RANGE'.
    """
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    recent_high = highs[-1]
    prev_high = max(highs[-10:-1])
    recent_low = lows[-1]
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
    Analyse LTF (Low Time Frame) for entry based on HTF bias.
    Returns a dictionary with trade info or None.
    """
    if len(candles) < 60:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # Supply / Demand zones
    supply = max(highs[-30:-5])
    demand = min(lows[-30:-5])

    # Previous highs/lows for CHOCH / BOS
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # BEARISH SETUP
    if htf_bias == "BEARISH":
        if last_close < prev_low and supply > last_close:
            entry = last_close
            sl = supply
            tp = entry - 2 * (sl - entry)
            return {
                "direction": "SELL",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from supply in HTF bearish context"
            }

    # BULLISH SETUP
    if htf_bias == "BULLISH":
        if last_close > prev_high and demand < last_close:
            entry = last_close
            sl = demand
            tp = entry + 2 * (entry - sl)
            return {
                "direction": "BUY",
                "bias": htf_bias,
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "reason": "LTF CHOCH/BOS after reaction from demand in HTF bullish context"
            }

    return None

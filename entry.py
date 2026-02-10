import requests
from config import TWELVE_API_KEY

# -------------------------
# Fetch Candles (TwelveData API)
# -------------------------
def fetch_candles(symbol, timeframe, limit=100):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "outputsize": limit,
        "apikey": TWELVE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "values" in data:
            return list(reversed(data["values"]))
        else:
            print(f"Error fetching candles for {symbol}: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return None


# -------------------------
# Analyse HTF Structure
# -------------------------
def analyse_htf_structure(candles):
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
# Analyse LTF Entry with Role Reversal
# -------------------------
# flipped_sr: dict to track flipped S/R per symbol
flipped_sr = {}

def analyse_ltf_entry(symbol, candles, htf_bias):
    """
    Analyse LTF for entry using support/resistance and role reversal.
    Returns entry dict or None.
    """
    global flipped_sr

    if len(candles) < 60:
        return None

    if symbol not in flipped_sr:
        flipped_sr[symbol] = {"support": [], "resistance": []}

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    # Current support/resistance zones (recent 25 candles)
    resistance = max(highs[-30:-5])
    support = min(lows[-30:-5])

    # Previous highs/lows for CHOCH/BOS
    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    # Include flipped levels
    all_resistances = [resistance] + flipped_sr[symbol]["resistance"]
    all_supports = [support] + flipped_sr[symbol]["support"]

    # -------------------------
    # Update flipped levels
    # -------------------------
    # Bullish breakout -> resistance becomes support
    if last_close > resistance:
        flipped_sr[symbol]["support"].append(resistance)

    # Bearish breakout -> support becomes resistance
    if last_close < support:
        flipped_sr[symbol]["resistance"].append(support)

    # -------------------------
    # BEARISH SETUP
    # -------------------------
    if htf_bias == "BEARISH":
        for r in all_resistances:
            if last_close < prev_low and last_close < r:
                entry = last_close
                sl = r
                tp = entry - 2 * (sl - entry)
                return {
                    "direction": "SELL",
                    "bias": htf_bias,
                    "entry": round(entry, 5),
                    "sl": round(sl, 5),
                    "tp": round(tp, 5),
                    "reason": f"LTF CHOCH/BOS near resistance {r} in HTF bearish context"
                }

    # -------------------------
    # BULLISH SETUP
    # -------------------------
    if htf_bias == "BULLISH":
        for s in all_supports:
            if last_close > prev_high and last_close > s:
                entry = last_close
                sl = s
                tp = entry + 2 * (entry - sl)
                return {
                "direction": "BUY",
                    "bias": htf_bias,
                    "entry": round(entry, 5),
                    "sl": round(sl, 5),
                    "tp": round(tp, 5),
                    "reason": f"LTF CHOCH/BOS near support {s} in HTF bullish context"
                }

    return None

import requests
import time
from config import API_KEY

def fetch_candles(symbol: str, timeframe: str, limit: int = 100):
    """
    Fetch historical candle data from TwelveData.
    Handles free plan limits, errors, and validates symbols.
    
    Args:
        symbol (str): Trading pair, e.g., "EUR/USD", "GBP/USD", "XAU/USD"
        timeframe (str): Timeframe, e.g., "1min", "5min", "15min", "1h", "4h"
        limit (int): Number of candles to fetch
    
    Returns:
        list: List of candles as dictionaries with 'open', 'high', 'low', 'close', 'datetime'
              or None if data cannot be fetched.
    """
    base_url = "https://api.twelvedata.com/time_series"
    
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": API_KEY,
        "outputsize": limit
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()

        # Check for errors returned by TwelveData
        if "status" in data and data["status"] == "error":
            print(f"TwelveData error for {symbol}: {data.get('message', 'Unknown error')}")
            return None
        
        if "values" not in data or len(data["values"]) == 0:
            print(f"No data returned for {symbol}")
            return None

        # Convert candles to correct format
        candles = [
            {
                "datetime": c["datetime"],
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"])
            }
            for c in reversed(data["values"])  # oldest first
        ]

        # Respect free plan rate limit: 1 request/sec
        time.sleep(1.2)

        return candles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching candles for {symbol}: {e}")
        return None

# -------------------------
# ANALYZE HTF STRUCTURE
# -------------------------
def analyse_htf_structure(candles):
    if not candles or len(candles) < 2:
        return "RANGE"

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    recent_high = highs[-1]
    prev_high = highs[-2]
    recent_low = lows[-1]
    prev_low = lows[-2]

    if recent_high > prev_high and recent_low > prev_low:
        return "BULLISH"
    elif recent_high < prev_high and recent_low < prev_low:
        return "BEARISH"
    else:
        return "RANGE"

# -------------------------
# ANALYZE LTF ENTRY
# -------------------------
def analyse_ltf_entry(candles, htf_bias):
    if len(candles) < 10:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    last_close = closes[-1]

    prev_high = max(highs[-10:-5])
    prev_low = min(lows[-10:-5])

    support = min(lows[-10:])
    resistance = max(highs[-10:])

    # Multi-condition confirmation
    conditions_met = 0

    # Condition 1: Candle retest above previous LTF high for bullish
    if htf_bias == "BULLISH" and last_close > prev_high and last_close <= resistance:
        conditions_met += 1

    # Condition 2: Candle retest near support
    if htf_bias == "BULLISH" and last_close <= support:
        conditions_met += 1

    # Condition 3: Price above previous HH (CHoCH confirmation)
    if htf_bias == "BULLISH" and last_close > prev_high:
        conditions_met += 1

    # Condition 4: Price bounce off zone (support/resistance)
    if htf_bias == "BULLISH" and last_close <= support:
        conditions_met += 1

    # Condition 5: Candle retest below previous LTF low for bearish
    if htf_bias == "BEARISH" and last_close < prev_low and last_close >= support:
        conditions_met += 1

    # Condition 6: Candle retest near resistance
    if htf_bias == "BEARISH" and last_close >= resistance:
        conditions_met += 1

    # Condition 7: Price below previous LL (CHoCH confirmation)
    if htf_bias == "BEARISH" and last_close < prev_low:
        conditions_met += 1

    # Condition 8: Price bounce off zone (support/resistance)
    if htf_bias == "BEARISH" and last_close >= resistance:
        conditions_met += 1

    if conditions_met < 2:  # Minimum conditions required
        return None

    # Calculate dynamic SL/TP
    if htf_bias == "BULLISH":
        entry = last_close
        sl = support
        tp = max(highs[-10:])  # Next swing high
        reason = "LTF retest bullish in HTF bullish context"
        direction = "BUY"
    elif htf_bias == "BEARISH":
        entry = last_close
        sl = resistance
        tp = min(lows[-10:])  # Next swing low
        reason = "LTF retest bearish in HTF bearish context"
        direction = "SELL"
    else:
        return None

    return {
        "direction": direction,
        "bias": htf_bias,
        "entry": round(entry, 5),
        "sl": round(sl, 5),
        "tp": round(tp, 5),
        "reason": reason
    }

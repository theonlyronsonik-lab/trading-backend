"""
structure.py
Market structure + BOS / CHoCH detection
"""

def analyze_structure(candles):
    """
    candles: list of OHLC dicts

    Returns dict:
    {
        "bias": "BULLISH" | "BEARISH" | "RANGE",
        "event": "BOS" | "CHOCH" | None
    }
    """

    if not candles or len(candles) < 30:
        return {"bias": "INSUFFICIENT_DATA", "event": None}

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    # Swing structure
    prev_high = max(highs[-20:-10])
    prev_low = min(lows[-20:-10])

    recent_high = max(highs[-10:])
    recent_low = min(lows[-10:])

    bias = "RANGE"
    event = None

    # Bullish BOS
    if recent_high > prev_high and recent_low > prev_low:
        bias = "BULLISH"
        event = "BOS"

    # Bearish BOS
    elif recent_low < prev_low and recent_high < prev_high:
        bias = "BEARISH"
        event = "BOS"

    # CHoCH conditions
    elif recent_high > prev_high and recent_low < prev_low:
        bias = "RANGE"
        event = "CHOCH"

    return {
        "bias": bias,
        "event": event
    }

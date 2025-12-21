def get_structure_levels(candles, direction):
    if direction == "bullish":
        lows = [float(c["low"]) for c in candles[-10:]]
        return min(lows)
    else:
        highs = [float(c["high"]) for c in candles[-10:]]
        return max(highs)
        def detect_bos(candles):
    """
    Detect Break of Structure (BOS)
    candles: list of dicts with open, high, low, close
    """
    if len(candles) < 3:
        return None

    prev = candles[-3]
    last = candles[-2]

    # Bullish BOS
    if last["close"] > prev["high"]:
        return "bullish"

    # Bearish BOS
    if last["close"] < prev["low"]:
        return "bearish"

    return None


def get_structure_levels(candles):
    """
    Return recent swing high and low
    """
    highs = [c["high"] for c in candles[-20:]]
    lows = [c["low"] for c in candles[-20:]]

    return {
        "swing_high": max(highs),
        "swing_low": min(lows)
        }


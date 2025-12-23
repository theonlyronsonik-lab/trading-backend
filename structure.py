def detect_market_structure(candles):
    """
    candles: list of dicts with keys: open, high, low, close
    Returns dict or None
    """

    if len(candles) < 5:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    last_high = highs[-1]
    prev_high = max(highs[:-1])

    last_low = lows[-1]
    prev_low = min(lows[:-1])

    if last_high > prev_high:
        return {
            "bias": "Bullish",
            "BOS": "Bullish Break of Structure",
            "level": prev_high
        }

    if last_low < prev_low:
        return {
            "bias": "Bearish",
            "BOS": "Bearish Break of Structure",
            "level": prev_low
        }

    return {
        "bias": "Range",
        "BOS": None,
        "level": None
    }

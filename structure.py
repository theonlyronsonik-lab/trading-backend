# structure.py

def detect_bos(candles):
    """
    Detect Break of Structure (BOS)
    candles: list of dicts with keys ['open','high','low','close']
    """
    if not candles or len(candles) < 3:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    last_close = candles[-1]["close"]

    if last_close > max(highs[:-1]):
        return "bullish"

    if last_close < min(lows[:-1]):
        return "bearish"

    return None


def get_structure_levels(candles):
    """
    Return recent swing high and swing low
    """
    if not candles or len(candles) < 5:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    return {
        "swing_high": max(highs),
        "swing_low": min(lows)
    }

# structure.py
# Market Structure logic for XAUUSD (HTF = 1H)

def get_structure_levels(candles, lookback=20):
    """
    Returns recent swing high and swing low
    candles: list of dicts with keys open, high, low, close
    """
    if len(candles) < lookback:
        return None

    recent = candles[-lookback:]

    swing_high = max(c["high"] for c in recent)
    swing_low = min(c["low"] for c in recent)

    return {
        "swing_high": swing_high,
        "swing_low": swing_low
    }


def detect_bos(candles, lookback=20):
    """
    Detect Break of Structure (BOS)
    Returns: 'bullish', 'bearish', or None
    """
    if len(candles) < lookback + 2:
        return None

    structure = get_structure_levels(candles[:-1], lookback)
    if not structure:
        return None

    last_candle = candles[-1]

    # Bullish BOS: close above previous swing high
    if last_candle["close"] > structure["swing_high"]:
        return "bullish"

    # Bearish BOS: close below previous swing low
    if last_candle["close"] < structure["swing_low"]:
        return "bearish"

    return None

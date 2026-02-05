# structure.py

def get_structure_bias(candles):
    """
    Determines market structure bias based on highs and lows
    candles: list of dicts with 'high' and 'low'
    """

    if len(candles) < 20:
        return "NOT_ENOUGH_DATA"

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    recent_highs = highs[-5:]
    recent_lows = lows[-5:]

    prev_highs = highs[-10:-5]
    prev_lows = lows[-10:-5]

    higher_high = max(recent_highs) > max(prev_highs)
    higher_low = min(recent_lows) > min(prev_lows)

    lower_high = max(recent_highs) < max(prev_highs)
    lower_low = min(recent_lows) < min(prev_lows)

    if higher_high and higher_low:
        return "BULLISH"

    if lower_high and lower_low:
        return "BEARISH"

    return "RANGE"

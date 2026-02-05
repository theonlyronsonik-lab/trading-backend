# structure.py

def get_structure_bias(candles):
    if len(candles) < 30:
        return "RANGE"

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    prev_high = max(highs[-30:-15])
    prev_low = min(lows[-30:-15])

    recent_high = max(highs[-15:])
    recent_low = min(lows[-15:])

    if recent_high > prev_high and recent_low > prev_low:
        return "BULLISH"

    if recent_low < prev_low and recent_high < prev_high:
        return "BEARISH"

    return "RANGE"

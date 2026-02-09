def get_structure_bias(candles):
    if not candles or len(candles) < 5:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    if highs[-1] > highs[-3] and lows[-1] > lows[-3]:
        return "bullish"

    if highs[-1] < highs[-3] and lows[-1] < lows[-3]:
        return "bearish"

    return "range"

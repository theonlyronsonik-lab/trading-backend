def get_structure_bias(candles):
    if len(candles) < 10:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
        return "bullish"

    if highs[-1] < highs[-2] and lows[-1] < lows[-2]:
        return "bearish"

    return None

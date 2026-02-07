def get_structure_bias(candles):
    if len(candles) < 20:
        return None

    highs = [float(c["high"]) for c in candles[-20:]]
    lows = [float(c["low"]) for c in candles[-20:]]

    if highs[-1] > highs[0] and lows[-1] > lows[0]:
        return "bullish"

    if highs[-1] < highs[0] and lows[-1] < lows[0]:
        return "bearish"

    return "range"

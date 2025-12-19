def detect_bos(candles):
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    if highs[-1] > max(highs[:-3]):
        return "bullish"
    if lows[-1] < min(lows[:-3]):
        return "bearish"
    return None


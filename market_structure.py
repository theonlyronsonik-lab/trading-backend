def detect_bos(candles):
    if len(candles) < 5:
        return None

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    if candles[-1]["close"] > max(highs[:-1]):
        return "BULLISH"

    if candles[-1]["close"] < min(lows[:-1]):
        return "BEARISH"

    return None

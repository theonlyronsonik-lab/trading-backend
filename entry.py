def retest_entry(candles, bias):
    closes = [float(c["close"]) for c in candles]
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]

    if bias == "bullish":
        if closes[-2] > highs[-3] and lows[-1] <= highs[-3]:
            return float(closes[-1])

    if bias == "bearish":
        if closes[-2] < lows[-3] and highs[-1] >= lows[-3]:
            return float(closes[-1])

    return None

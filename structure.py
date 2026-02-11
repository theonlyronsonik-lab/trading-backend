def get_htf_bias(candles):
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    if closes[-1] > highs[-2]:
        return "bullish"

    if closes[-1] < lows[-2]:
        return "bearish"

    return None


def detect_choch(candles, bias):
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    if bias == "bullish":
        if closes[-1] > highs[-2]:
            return True

    if bias == "bearish":
        if closes[-1] < lows[-2]:
            return True

    return False

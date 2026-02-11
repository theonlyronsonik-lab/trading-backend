def get_next_swing_high(candles):
    highs = [float(c["high"]) for c in candles]
    return max(highs[-10:])


def get_next_swing_low(candles):
    lows = [float(c["low"]) for c in candles]
    return min(lows[-10:])

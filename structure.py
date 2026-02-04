def get_swings(candles, lookback=3):
    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(candles) - lookback):
        high = candles[i]["high"]
        low = candles[i]["low"]

        if high == max(c["high"] for c in candles[i-lookback:i+lookback+1]):
            swing_highs.append((i, high))

        if low == min(c["low"] for c in candles[i-lookback:i+lookback+1]):
            swing_lows.append((i, low))

    return swing_highs, swing_lows


def get_market_bias(candles):
    swing_highs, swing_lows = get_swings(candles)

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return "NEUTRAL"

    last_high = swing_highs[-1][1]
    prev_high = swing_highs[-2][1]

    last_low = swing_lows[-1][1]
    prev_low = swing_lows[-2][1]

    if last_high > prev_high and last_low > prev_low:
        return "BULLISH"
    elif last_high < prev_high and last_low < prev_low:
        return "BEARISH"
    else:
        return "RANGING"


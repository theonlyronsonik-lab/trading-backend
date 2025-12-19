def detect_liquidity(candles):
    if len(candles) < 10:
        return None

    highs = [c["high"] for c in candles[:-1]]
    lows = [c["low"] for c in candles[:-1]]

    last = candles[-1]

    if last["high"] > max(highs):
        return "sweep_high"

    if last["low"] < min(lows):
        return "sweep_low"

    return None

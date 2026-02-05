# liquidity.py

def detect_liquidity_sweep(candles):
    if len(candles) < 20:
        return None

    prev = candles[-10:-5]
    last = candles[-1]

    prev_high = max(c["high"] for c in prev)
    prev_low = min(c["low"] for c in prev)

    if last["high"] > prev_high and last["close"] < prev_high:
        return "BUY_SIDE"

    if last["low"] < prev_low and last["close"] > prev_low:
        return "SELL_SIDE"

    return None

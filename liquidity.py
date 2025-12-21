# liquidity.py

def liquidity_sweep(candles):
    """
    Detect liquidity sweep:
    - Price takes previous high/low
    - Then closes back inside range
    """
    if not candles or len(candles) < 3:
        return None

    prev = candles[-2]
    last = candles[-1]

    # Buy-side liquidity sweep
    if last["high"] > prev["high"] and last["close"] < prev["high"]:
        return "buy_side"

    # Sell-side liquidity sweep
    if last["low"] < prev["low"] and last["close"] > prev["low"]:
        return "sell_side"

    return None

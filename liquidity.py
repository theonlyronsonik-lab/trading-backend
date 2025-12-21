# liquidity.py

def liquidity_sweep(candles, structure_levels):
    """
    Detect liquidity sweep near support/resistance levels.
    Returns True if sweep occurs, otherwise False.
    """
    if not candles or not structure_levels:
        return False

    last_candle = candles[-1]
    support = structure_levels["support"]
    resistance = structure_levels["resistance"]

    # Check if candle touches or slightly breaks support/resistance
    if last_candle['low'] <= support * 0.995:
        return True  # liquidity taken below support
    if last_candle['high'] >= resistance * 1.005:
        return True  # liquidity taken above resistance

    return False

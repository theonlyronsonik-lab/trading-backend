# structure.py

def get_structure_levels(candles):
    """
    Identify key support and resistance levels based on candle highs/lows.
    Returns a list of structure levels.
    """
    if not candles:
        return []

    highs = [candle['high'] for candle in candles]
    lows = [candle['low'] for candle in candles]

    resistance = max(highs)
    support = min(lows)

    return {
        "support": support,
        "resistance": resistance
    }


def detect_bos(candles):
    """
    Detect Break of Structure (BOS) in the market.
    Returns True if BOS is detected, otherwise False.
    """
    if len(candles) < 2:
        return False

    last_close = candles[-1]['close']
    prev_high = candles[-2]['high']
    prev_low = candles[-2]['low']

    # Simple bullish/bearish BOS logic
    if last_close > prev_high or last_close < prev_low:
        return True

    return False

"""
structure.py
Handles market structure bias detection.
No circular imports. No side effects.
"""

def get_structure_bias(candles):
    """
    Determines market structure bias based on highs and lows.

    candles: list of dicts with keys:
        - open
        - high
        - low
        - close

    Returns:
        "BULLISH", "BEARISH", or "RANGE"
    """

    # Safety check
    if not candles or len(candles) < 20:
        return "INSUFFICIENT_DATA"

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    # Recent structure
    recent_highs = highs[-5:]
    recent_lows = lows[-5:]

    prev_highs = highs[-10:-5]
    prev_lows = lows[-10:-5]

    # Higher High + Higher Low → Bullish
    if max(recent_highs) > max(prev_highs) and min(recent_lows) > min(prev_lows):
        return "BULLISH"

    # Lower High + Lower Low → Bearish
    if max(recent_highs) < max(prev_highs) and min(recent_lows) < min(prev_lows):
        return "BEARISH"

    # Otherwise → Range / Chop
    return "RANGE"


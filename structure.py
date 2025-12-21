def get_structure_levels(candles, direction):
    if direction == "bullish":
        lows = [float(c["low"]) for c in candles[-10:]]
        return min(lows)
    else:
        highs = [float(c["high"]) for c in candles[-10:]]
        return max(highs)


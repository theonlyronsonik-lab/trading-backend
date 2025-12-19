def calculate_sl_tp(entry, sweep_level, structure_level, direction):
    if direction == "bullish":
        sl = min(sweep_level, structure_level)
        tp1 = entry + (entry - sl) * 1.5
        tp2 = entry + (entry - sl) * 3
    else:
        sl = max(sweep_level, structure_level)
        tp1 = entry - (sl - entry) * 1.5
        tp2 = entry - (sl - entry) * 3

    return sl, tp1, tp2

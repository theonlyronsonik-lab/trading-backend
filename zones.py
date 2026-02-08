def get_supply_demand_zones(candles, lookback=50):
    """
    Detect basic supply and demand zones from recent candles.

    candles: list of OHLC dicts
    lookback: number of candles to inspect
    """

    supply_zones = []
    demand_zones = []

    if not candles or len(candles) < lookback:
        return {"supply": supply_zones, "demand": demand_zones}

    recent = candles[-lookback:]

    for i in range(2, len(recent) - 2):

        high = float(recent[i]["high"])
        low = float(recent[i]["low"])

        prev_high = float(recent[i - 1]["high"])
        next_high = float(recent[i + 1]["high"])

        prev_low = float(recent[i - 1]["low"])
        next_low = float(recent[i + 1]["low"])

        # -----------------------------
        # SUPPLY ZONE (swing high)
        # -----------------------------
        if high > prev_high and high > next_high:
            supply_zones.append({
                "price": high,
                "index": i
            })

        # -----------------------------
        # DEMAND ZONE (swing low)
        # -----------------------------
        if low < prev_low and low < next_low:
            demand_zones.append({
                "price": low,
                "index": i
            })

    return {
        "supply": supply_zones[-3:],   # keep most recent zones only
        "demand": demand_zones[-3:]
    }

def calculate_sl_tp(
    bias,
    entry_price,
    structure_levels,
    zones,
    min_rr=3
):
    """
    Calculate Stop Loss and Take Profit based on:
    - Market bias (bullish / bearish)
    - Market structure (swing high / low)
    - Supply & demand zones
    - Minimum Risk:Reward (default 1:3)

    Returns:
        dict with sl, tp, rr
        OR None if RR < min_rr
    """

    sl = None
    tp = None

    # -------------------------
    # BULLISH SCENARIO
    # -------------------------
    if bias == "bullish":
        swing_low = structure_levels.get("last_swing_low")
        demand_zones = zones.get("demand", [])

        if not swing_low:
            return None

        sl = swing_low

        # Prefer TP at nearest supply zone
        if demand_zones:
            # For bullish, TP should be ABOVE entry → supply zone
            supply_zones = zones.get("supply", [])
            valid_supply = [
                z["price"] for z in supply_zones if z["price"] > entry_price
            ]
            if valid_supply:
                tp = min(valid_supply)

        # Fallback TP: structure-based
        if not tp:
            tp = entry_price + (entry_price - sl) * min_rr

    # -------------------------
    # BEARISH SCENARIO
    # -------------------------
    elif bias == "bearish":
        swing_high = structure_levels.get("last_swing_high")
        supply_zones = zones.get("supply", [])

        if not swing_high:
            return None

        sl = swing_high

        # Prefer TP at nearest demand zone
        if supply_zones:
            demand_zones = zones.get("demand", [])
            valid_demand = [
                z["price"] for z in demand_zones if z["price"] < entry_price
            ]
            if valid_demand:
                tp = max(valid_demand)

        # Fallback TP: structure-based
        if not tp:
            tp = entry_price - (sl - entry_price) * min_rr

    else:
        return None

    # -------------------------
    # Risk Reward Check
    # -------------------------
    risk = abs(entry_price - sl)
    reward = abs(tp - entry_price)

    if risk == 0:
        return None

    rr = round(reward / risk, 2)

    if rr < min_rr:
        return None

    return {
        "sl": round(sl, 5),
        "tp": round(tp, 5),
        "rr": rr
    }

def calculate_position(entry, stop, balance=10000, risk_percent=1):
    """
    Simple risk model (display purposes)
    """
    risk_amount = balance * (risk_percent / 100)
    stop_distance = abs(entry - stop)

    if stop_distance == 0:
        return None

    lot_size = risk_amount / stop_distance
    rr_target = entry + (stop_distance * 2)

    return {
        "risk_%": risk_percent,
        "lot_size": round(lot_size, 2),
        "rr": "1:2",
        "tp": round(rr_target, 2)
    }

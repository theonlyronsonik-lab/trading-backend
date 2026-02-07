def detect_supply_demand(candles):
    zones = []

    for i in range(2, len(candles) - 2):
        prev = candles[i - 1]
        curr = candles[i]
        next_ = candles[i + 1]

        # SUPPLY ZONE
        if (
            float(prev["close"]) > float(prev["open"]) and
            float(curr["close"]) < float(curr["open"]) and
            float(next_["close"]) < float(next_["open"])
        ):
            zones.append({
                "type": "supply",
                "high": float(curr["high"]),
                "low": float(curr["low"])
            })

        # DEMAND ZONE
        if (
            float(prev["close"]) < float(prev["open"]) and
            float(curr["close"]) > float(curr["open"]) and
            float(next_["close"]) > float(next_["open"])
        ):
            zones.append({
                "type": "demand",
                "high": float(curr["high"]),
                "low": float(curr["low"])
            })

    return zones


def price_in_zone(price, zone):
    return zone["low"] <= price <= zone["high"]

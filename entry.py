"""
LTF Entry Logic
- Uses market structure (HH/HL or LH/LL)
- Uses supply & demand zones
- Confirms with HTF bias
- Only valid if RR >= 1:3
"""

from typing import Optional, Dict, List


# -----------------------------
# Helpers
# -----------------------------

def is_bullish_structure(candles: List[dict]) -> bool:
    if len(candles) < 3:
        return False
    return candles[-1]["high"] > candles[-2]["high"] and candles[-1]["low"] > candles[-2]["low"]


def is_bearish_structure(candles: List[dict]) -> bool:
    if len(candles) < 3:
        return False
    return candles[-1]["low"] < candles[-2]["low"] and candles[-1]["high"] < candles[-2]["high"]


def find_demand_zone(candles: List[dict]) -> Optional[float]:
    """
    Simple demand zone:
    last strong bearish candle before bullish move
    """
    for i in range(len(candles) - 3, 0, -1):
        c = candles[i]
        if c["close"] < c["open"]:
            return c["low"]
    return None


def find_supply_zone(candles: List[dict]) -> Optional[float]:
    """
    Simple supply zone:
    last strong bullish candle before bearish move
    """
    for i in range(len(candles) - 3, 0, -1):
        c = candles[i]
        if c["close"] > c["open"]:
            return c["high"]
    return None


def rr_is_valid(entry: float, sl: float, tp: float, rr_min: float = 3.0) -> bool:
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    if risk == 0:
        return False
    return (reward / risk) >= rr_min


# -----------------------------
# MAIN ENTRY FUNCTION
# -----------------------------

def find_ltf_entry(
    candles: List[dict],
    htf_bias: str
) -> Optional[Dict]:
    """
    Returns:
    {
        "type": "BUY" | "SELL",
        "entry": float,
        "sl": float,
        "tp": float,
        "rr": float
    }
    or None
    """

    if len(candles) < 10:
        return None

    last_price = candles[-1]["close"]

    # -------------------------
    # BULLISH SETUP
    # -------------------------
    if htf_bias == "BULLISH" and is_bullish_structure(candles):
        demand = find_demand_zone(candles)
        if not demand:
            return None

        entry = last_price
        sl = demand
        supply = find_supply_zone(candles)

        if not supply:
            return None

        tp = supply

        if rr_is_valid(entry, sl, tp):
            rr = abs(tp - entry) / abs(entry - sl)
            return {
                "type": "BUY",
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "rr": round(rr, 2)
            }

    # -------------------------
    # BEARISH SETUP
    # -------------------------
    if htf_bias == "BEARISH" and is_bearish_structure(candles):
        supply = find_supply_zone(candles)
        if not supply:
            return None

        entry = last_price
        sl = supply
        demand = find_demand_zone(candles)

        if not demand:
            return None

        tp = demand

        if rr_is_valid(entry, sl, tp):
            rr = abs(entry - tp) / abs(sl - entry)
            return {
                "type": "SELL",
                "entry": round(entry, 5),
                "sl": round(sl, 5),
                "tp": round(tp, 5),
                "rr": round(rr, 2)
            }

    return None

# risk.py

def calculate_lot_size(balance, entry, sl, risk_percent):
    risk_amount = balance * risk_percent
    stop_distance = abs(entry - sl)

    if stop_distance == 0:
        return 0

    lot = risk_amount / stop_distance
    return round(lot, 2)

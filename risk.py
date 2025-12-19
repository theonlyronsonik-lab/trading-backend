from config import ACCOUNT_BALANCE, RISK_PERCENT, RR_RATIO

def calculate_trade(entry, stop, direction):
    risk_amount = ACCOUNT_BALANCE * (RISK_PERCENT / 100)
    risk_pips = abs(entry - stop)

    if risk_pips == 0:
        return None

    if direction == "BUY":
        take_profit = entry + (risk_pips * RR_RATIO)
    else:
        take_profit = entry - (risk_pips * RR_RATIO)

    return {
        "entry": round(entry, 2),
        "stop": round(stop, 2),
        "tp": round(take_profit, 2),
        "risk": risk_amount
    }

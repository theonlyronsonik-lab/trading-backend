from data_feed import get_price
from structure import detect_bos, get_structure_levels
from liquidity import liquidity_sweep, liquidity_sweep_level
from scoring import score_setup
from notifier import send_alert
from config import SCORE_THRESHOLD
from risk import calculate_sl_tp

def run():
    candles = get_price()
    direction = detect_bos(candles)

    if not direction:
        return

    liquidity = liquidity_sweep(candles)
    score = score_setup(
        direction,
        direction,
        liquidity,
        zone_ok=True,
        session_ok=True,
        rr_ok=True
    )

    if score < SCORE_THRESHOLD:
        return

    entry = float(candles[-1]["close"])
    sweep_level = liquidity_sweep_level(candles, direction)
    structure_level = get_structure_levels(candles, direction)

    sl, tp1, tp2 = calculate_sl_tp(entry, sweep_level, structure_level, direction)

    message = (
        f"XAUUSD SIGNAL 🚨\n"
        f"Direction: {direction.upper()}\n"
        f"Entry: {entry}\n"
        f"SL: {sl}\n"
        f"TP1: {tp1}\n"
        f"TP2: {tp2}\n"
        f"Score: {score}/10"
    )

    send_alert(message)

if __name__ == "__main__":
    run()

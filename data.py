import MetaTrader5 as mt5
from datetime import datetime
import time


# =============================
# INIT MT5
# =============================
if not mt5.initialize():
    raise RuntimeError("❌ MT5 initialization failed")


# =============================
# TIMEFRAME MAP
# =============================
TF_MAP = {
    "1min": mt5.TIMEFRAME_M1,
    "5min": mt5.TIMEFRAME_M5,
    "15min": mt5.TIMEFRAME_M15,
    "30min": mt5.TIMEFRAME_M30,
    "1h": mt5.TIMEFRAME_H1,
    "4h": mt5.TIMEFRAME_H4,
    "1d": mt5.TIMEFRAME_D1,
}


# =============================
# GET CANDLES
# =============================
def get_candles(symbol, timeframe, limit=100):
    if timeframe not in TF_MAP:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    tf = TF_MAP[timeframe]

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, limit)

    if rates is None or len(rates) == 0:
        return []

    candles = []
    for r in rates:
        candles.append({
            "time": datetime.fromtimestamp(r["time"]),
            "open": float(r["open"]),
            "high": float(r["high"]),
            "low": float(r["low"]),
            "close": float(r["close"]),
            "volume": int(r["tick_volume"])
        })

    return candles

import os

_raw = os.getenv("SYMBOLS")

if _raw:
    SYMBOLS = [s.strip() for s in _raw.split(",") if s.strip()]
else:
    SYMBOLS = ["XAUUSD", "EURUSD"]

HTF = "4h"
LTF = "15min"

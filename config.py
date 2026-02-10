# =========================
# SYMBOLS & TIMEFRAMES
# =========================

SYMBOLS = [
    "GBP/USD",
    "EUR/USD",
    "XAU/USD",
]

HTF = "4h"
LTF = "15min"


# =========================
# ENTRY SETTINGS
# =========================

RR_RATIO = 3          # Risk : Reward
LOOKBACK_LTF = 120    # Candles to scan for structure
ZONE_BUFFER = 0.0005  # Small padding for zones (adjust for XAU)

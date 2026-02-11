import os

# ==============================
# API CONFIG
# ==============================
TWELVEDATA_API_KEY = os.getenv("d143e9bb8b0c4d7487872fd699280bde")

# ==============================
# PAIRS
# ==============================
PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "XAU/USD",
    "AUD/CAD"
]

# ==============================
# TIMEFRAMES
# ==============================
HTF = "4h"
LTF = "15min"

# ==============================
# SCANNING CONTROL
# ==============================
SCAN_INTERVAL = 60  # seconds between scans
HTF_CACHE = {}      # stores last HTF fetch time per pair

# ==============================
# TRADING SETTINGS
# ==============================
RISK_PER_TRADE = 0.01
RR_MIN = 2

# ==============================
# TELEGRAM
# ==============================
TELEGRAM_TOKEN = os.getenv("8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc")
TELEGRAM_CHAT_ID = os.getenv("6599172354")

PAIR_STATE = {}
